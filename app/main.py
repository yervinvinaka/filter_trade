import time
import logging

from app.services.market_service import MarketPosition

from app.services.strategy_service import (
    process_market_data
)

from app.services.volatility_service import (
    analyze_volatility
)

from app.services.risk_service import (
    calculate_atr,
    calculate_trade_levels
)

from app.services.confidence_service import (
    calculate_confidence,
    get_setup_type
)

from app.services.interpreter_service import (
    interpret_signal
)

from app.services.multi_timeframe_service import (
    analyze_multi_timeframe
)

from app.services.trade_tracker_service import (
    save_trade,
    check_open_trades,
    close_trade
)

from app.services.confirmation_service import (
    confirm_trade
)

from app.alerts.alert_service import send_alert


print("🔥 BOT ARRANCANDO EN RAILWAY")


# ==================================================
# 🔹 LOGS
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ==================================================
# 🔹 SYMBOLS
# ==================================================

symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "LINKUSDT"
]


# ==================================================
# 🔥 ANTI-SPAM
# ==================================================

last_signals = {}

last_volatility_alert = {}

last_heartbeat = 0


# ==================================================
# 🔥 MAIN LOOP
# ==================================================

def run_bot():

    global last_heartbeat

    logging.info("🚀 Bot iniciado...")

    market = MarketPosition()

    while True:

        try:

            logging.info("📊 Analizando mercado...")

            for symbol in symbols:

                try:

                    # ==================================================
                    # 🔹 MARKET DATA
                    # ==================================================

                    data = market.fetch_data(symbol)

                    if not data:
                        continue

                    oi = data["open_interest"]

                    funding = data["funding_rate"]

                    closes = data["closes"]

                    klines = data["klines"]

                    # ==================================================
                    # 🔥 MULTI TIMEFRAME
                    # ==================================================

                    mtf = analyze_multi_timeframe(
                        symbol
                    )

                    alignment = None

                    if mtf:
                        alignment = mtf["alignment"]

                    # ==================================================
                    # 🔥 STRATEGY
                    # ==================================================

                    result = process_market_data(
                        symbol,
                        closes,
                        klines,
                        mtf
                    )

                    if not result:
                        continue

                    signal = result["signal"]

                    rsi = result["rsi"]

                    ema_signal = result["ema_signal"]

                    movement = result["movement"]

                    # ==================================================
                    # 🔥 VOLATILITY
                    # ==================================================

                    volatility = analyze_volatility(
                        klines,
                        oi
                    )

                    # ==================================================
                    # 🔥 CONFIRMATION ENGINE
                    # ==================================================

                    confirmation = confirm_trade(
                        closes,
                        klines
                    )

                    # ==================================================
                    # 🔥 INVALID SIGNAL FILTER
                    # ==================================================

                    if (
                        signal
                        and not confirmation["valid"]
                    ):

                        logging.info(
                            f"⛔ Señal descartada "
                            f"por confirmation engine "
                            f"en {symbol}"
                        )

                        signal = None

                    # ==================================================
                    # 🔥 ATR + RISK
                    # ==================================================

                    current_price = float(
                        klines[-1][4]
                    )

                    atr = calculate_atr(
                        klines
                    )

                    trade_levels = calculate_trade_levels(
                        signal,
                        current_price,
                        atr
                    )

                    # ==================================================
                    # 🔥 CONFIDENCE
                    # ==================================================

                    confidence = None

                    interpretation = None

                    setup_type = None

                    if signal:

                        confidence = calculate_confidence(
                            signal,
                            rsi,
                            ema_signal,
                            funding,
                            alignment,
                            volatility,
                            movement
                        )

                        interpretation = interpret_signal(
                            signal,
                            rsi,
                            ema_signal,
                            confidence,
                            movement,
                            volatility
                        )

                        setup_type = get_setup_type(
                            signal,
                            ema_signal,
                            alignment
                        )

                    # ==================================================
                    # 🔹 LOGS
                    # ==================================================

                    rsi_value = (
                        round(rsi, 2)
                        if rsi
                        else 0
                    )

                    logging.info(
                        f"{symbol} | "
                        f"RSI: {rsi_value} | "
                        f"EMA: {ema_signal} | "
                        f"Funding: {funding:.6f} | "
                        f"OI: {oi:.2f} | "
                        f"Confirmations: "
                        f"{confirmation['score']}/3"
                    )

                    # ==================================================
                    # 🔥 SIGNAL ALERT
                    # ==================================================

                    if (
                        signal
                        and last_signals.get(symbol)
                        != signal
                    ):

                        last_signals[symbol] = signal

                        emoji = "🟢"

                        if "SELL" in signal:
                            emoji = "🔴"

                        # ==================================================
                        # 🔥 SETUP EMOJI
                        # ==================================================

                        setup_emoji = "⚪"

                        if setup_type == "TREND_CONTINUATION":
                            setup_emoji = "🟢"

                        elif setup_type == "COUNTER_TREND":
                            setup_emoji = "🟠"

                        elif setup_type == "MIXED_SETUP":
                            setup_emoji = "🟡"

                        # ==================================================
                        # 🔥 BASE MESSAGE
                        # ==================================================

                        message = (
                            f"{emoji} SIGNAL ALERT\n\n"

                            f"📊 Symbol: {symbol}\n"

                            f"📈 Signal: {signal}\n"

                            f"📉 RSI: {rsi_value}\n"

                            f"📊 EMA Trend: {ema_signal}\n"

                            f"💰 Funding: {funding:.6f}\n"

                            f"📦 OI: {oi:.2f}"
                        )

                        # ==================================================
                        # 🔥 CONFIRMATION SCORE
                        # ==================================================

                        message += (
                            f"\n\n"
                            f"✅ Confirmation Engine\n\n"

                            f"🎯 Confirmations: "
                            f"{confirmation['score']}/3"
                        )

                        # ==================================================
                        # 🔥 MULTI TIMEFRAME INFO
                        # ==================================================

                        if mtf:

                            message += (
                                f"\n\n"
                                f"🧠 Multi-Timeframe\n\n"

                                f"⏱️ 1H: "
                                f"{mtf['1h']}\n"

                                f"⏱️ 4H: "
                                f"{mtf['4h']}\n"

                                f"⏱️ 1D: "
                                f"{mtf['1d']}\n\n"

                                f"🎯 Alignment: "
                                f"{mtf['alignment']}"
                            )

                        # ==================================================
                        # 🔥 SETUP TYPE
                        # ==================================================

                        if setup_type:

                            message += (
                                f"\n\n"
                                f"{setup_emoji} Setup Type\n\n"

                                f"{setup_type}"
                            )

                        # ==================================================
                        # 🔥 TRADE LEVELS
                        # ==================================================

                        if trade_levels:

                            message += (
                                f"\n\n"
                                f"🎯 Entry: "
                                f"{trade_levels['entry']}\n"

                                f"🛑 SL: "
                                f"{trade_levels['stop_loss']}\n"

                                f"💰 TP: "
                                f"{trade_levels['take_profit']}\n"

                                f"📈 R:R: "
                                f"{trade_levels['risk_reward']}\n"

                                f"📊 ATR: "
                                f"{trade_levels['atr']}"
                            )

                            # ==================================================
                            # 🔥 SAVE TRADE
                            # ==================================================

                            save_trade(
                                symbol,
                                signal,
                                trade_levels["entry"],
                                trade_levels["stop_loss"],
                                trade_levels["take_profit"]
                            )

                        # ==================================================
                        # 🔥 CONFIDENCE
                        # ==================================================

                        if confidence:

                            confidence_emoji = "🟢"

                            if (
                                confidence["level"]
                                == "MEDIUM"
                            ):
                                confidence_emoji = "🟡"

                            elif (
                                confidence["level"]
                                == "LOW"
                            ):
                                confidence_emoji = "🔴"

                            message += (
                                f"\n\n"
                                f"{confidence_emoji} Confidence\n\n"

                                f"🎯 Score: "
                                f"{confidence['score']}%\n"

                                f"📊 Strength: "
                                f"{confidence['level']}"
                            )

                        # ==================================================
                        # 🔥 MOVEMENT
                        # ==================================================

                        if movement:

                            message += (
                                f"\n\n"
                                f"🚨 "
                                f"{movement['type']} "
                                f"DETECTED\n"

                                f"⚡ Change: "
                                f"{movement['change_pct']}%"
                            )

                        # ==================================================
                        # 🔥 INTERPRETATION
                        # ==================================================

                        if interpretation:

                            message += (
                                f"\n\n"
                                f"💡 Market Interpretation\n\n"
                                f"{interpretation}"
                            )

                        # ==================================================
                        # 🔥 WARNING COUNTER TREND
                        # ==================================================

                        if (
                            setup_type
                            == "COUNTER_TREND"
                        ):

                            message += (
                                f"\n\n"
                                f"⚠️ WARNING\n\n"

                                f"This setup is "
                                f"against the main trend.\n"

                                f"Higher risk of failure."
                            )

                        # ==================================================
                        # 🔥 PREMIUM SETUP
                        # ==================================================

                        if (
                            confidence
                            and confidence["score"] >= 80
                        ):

                            message += (
                                f"\n\n"
                                f"🔥 PREMIUM SETUP "
                                f"DETECTED"
                            )

                        # ==================================================
                        # 🔥 SEND ALERT
                        # ==================================================

                        logging.info(
                            f"📩 Enviando SIGNAL ALERT: "
                            f"{symbol}"
                        )

                        send_alert(message)

                    else:

                        logging.info(
                            f"⏸️ Sin nueva señal válida en "
                            f"{symbol}"
                        )

                    # ==================================================
                    # 🔥 VOLATILITY ALERTS
                    # ==================================================

                    if (
                        volatility
                        and volatility["score"] >= 60
                    ):

                        volatility_key = (
                            f"{symbol}_"
                            f"{volatility['event']}"
                        )

                        if (
                            last_volatility_alert.get(symbol)
                            != volatility_key
                        ):

                            last_volatility_alert[symbol] = (
                                volatility_key
                            )

                            volatility_msg = (
                                f"⚠️ HIGH VOLATILITY "
                                f"DETECTED\n\n"

                                f"📊 Symbol: "
                                f"{symbol}\n"

                                f"🔥 Event: "
                                f"{volatility['event']}\n"

                                f"⚡ Strength: "
                                f"{volatility['strength']}\n"

                                f"📈 Price Change: "
                                f"{volatility['change_pct']}%\n"

                                f"📦 Volume Change: "
                                f"{volatility['volume_change']}%\n"

                                f"🎯 Score: "
                                f"{volatility['score']}"
                            )

                            logging.info(
                                f"🚨 Volatility alert: "
                                f"{symbol}"
                            )

                            send_alert(
                                volatility_msg
                            )

                except Exception as e:

                    logging.error(
                        f"❌ Error procesando "
                        f"{symbol}: {e}"
                    )

            # ==================================================
            # 🔥 CHECK OPEN TRADES
            # ==================================================

            open_trades = check_open_trades()

            for trade in open_trades:

                try:

                    if trade["status"] != "OPEN":
                        continue

                    trade_symbol = trade["symbol"]

                    trade_data = market.fetch_data(
                        trade_symbol
                    )

                    if not trade_data:
                        continue

                    current_price = float(
                        trade_data["klines"][-1][4]
                    )

                    signal_type = trade["signal"]

                    tp = trade["take_profit"]

                    sl = trade["stop_loss"]

                    # ==========================================
                    # BUY
                    # ==========================================

                    if "BUY" in signal_type:

                        if current_price >= tp:

                            close_trade(
                                trade,
                                "WIN"
                            )

                            send_alert(
                                f"✅ TAKE PROFIT HIT\n\n"
                                f"📊 {trade_symbol}\n"
                                f"💰 TP alcanzado\n"
                                f"📈 Resultado: WIN"
                            )

                        elif current_price <= sl:

                            close_trade(
                                trade,
                                "LOSS"
                            )

                            send_alert(
                                f"❌ STOP LOSS HIT\n\n"
                                f"📊 {trade_symbol}\n"
                                f"🛑 SL alcanzado\n"
                                f"📉 Resultado: LOSS"
                            )

                    # ==========================================
                    # SELL
                    # ==========================================

                    elif "SELL" in signal_type:

                        if current_price <= tp:

                            close_trade(
                                trade,
                                "WIN"
                            )

                            send_alert(
                                f"✅ TAKE PROFIT HIT\n\n"
                                f"📊 {trade_symbol}\n"
                                f"💰 TP alcanzado\n"
                                f"📈 Resultado: WIN"
                            )

                        elif current_price >= sl:

                            close_trade(
                                trade,
                                "LOSS"
                            )

                            send_alert(
                                f"❌ STOP LOSS HIT\n\n"
                                f"📊 {trade_symbol}\n"
                                f"🛑 SL alcanzado\n"
                                f"📉 Resultado: LOSS"
                            )

                except Exception as e:

                    logging.error(
                        f"❌ Error checking trade: {e}"
                    )

            # ==================================================
            # 🔥 HEARTBEAT
            # ==================================================

            current_time = time.time()

            if (
                current_time - last_heartbeat
                > 21600
            ):

                heartbeat_msg = (
                    "✅ BOT ONLINE\n\n"
                    "📊 Sistema funcionando "
                    "correctamente\n"
                    "🚀 Railway activo\n"
                    "📡 Monitoreando mercado "
                    "24/7"
                )

                send_alert(
                    heartbeat_msg
                )

                logging.info(
                    "✅ Heartbeat enviado"
                )

                last_heartbeat = current_time

            # ==================================================
            # 🔥 WAIT
            # ==================================================

            time.sleep(60)

        except Exception as e:

            logging.error(
                f"🔥 ERROR CRÍTICO LOOP: {e}"
            )

            time.sleep(30)


# ==================================================
# 🔥 ENTRYPOINT
# ==================================================

if __name__ == "__main__":

    run_bot()