from app.core.logger import logger
import random

def get_social_mentions(symbol):
    try:
        mentions = random.randint(0, 20)
        logger.info(f"{symbol} | Menciones sociales: {mentions}")
        return mentions

    except Exception as e:
        logger.error(f"{symbol} | Error social_service: {e}")
        return 0