import logging
from logging.handlers import TimedRotatingFileHandler
import config

logger = logging.getLogger("check-in-logger")


def setup_logger(is_local: bool):
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    if is_local:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        rotating_handler = logging.handlers.RotatingFileHandler(
            config.LOG_FILE,
            maxBytes=config.LOG_FILE_MAX_SIZE,
            backupCount=config.LOG_FILE_BACKUP_COUNT,
        )
        rotating_handler.setFormatter(formatter)
        logger.addHandler(rotating_handler)
