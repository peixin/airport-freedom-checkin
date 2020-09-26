from datetime import datetime
from .checkin import CheckInFactory
from .logger import logger, setup_logger


def main(is_local: bool):
    setup_logger(is_local)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logger.info(f"{'-' * 10}{now.center(len(now) + 2, ' ')}{'-' * 10}")
    check_in = CheckInFactory.instance(is_local)
    result = check_in.process()

    logger.info(f"{'-' * 10}{'end'.center(5, ' ')}{'-' * 10}\n")
    return result
