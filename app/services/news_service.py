import feedparser


def get_crypto_news():
    feeds = [
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cointelegraph.com/rss"
    ]

    news_list = []

    try:
        for feed_url in feeds:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:2]:  # 2 por fuente
                title = entry.title
                link = entry.link

                news_list.append(f"📰 {title}\n{link}")

        return news_list

    except Exception as e:
        print("❌ Error obteniendo noticias:", e)
        return []