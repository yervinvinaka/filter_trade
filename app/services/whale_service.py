from app.core.logger import logger

def detect_whale_activity(data):
    try:
        volumes = [float(candle["volume"]) for candle in data]

        if len(volumes) < 10:
            return False

        avg_volume = sum(volumes[:-1]) / (len(volumes) - 1)
        last_volume = volumes[-1]

        if last_volume > avg_volume * 2:
            logger.info("🐋 Whale detectada!")
            return True

        return False

    except Exception as e:
        logger.error(f"Error whale detection: {e}")
        return False