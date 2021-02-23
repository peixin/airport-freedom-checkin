import os
from datetime import datetime
from pytz import timezone
from typing import Tuple
import requests
import config
from .checkin import CheckInFactory
from .logger import logger, setup_logger


def get_version():
    try:
        with open(".version", "r") as f:
            return f.read().strip()
    except:
        return ""


def remind_by_wechat(is_local: bool, result_info: Tuple[bool, str, str]):
    result, title, message = result_info
    today = datetime.now(tz=timezone(config.TIMEZONE)).strftime("%Y.%m.%d")
    data = {"title": f"{today}, {title}", "desp": message}
    server_chan_key = os.environ.get("SERVER_CHAN_KEY")
    if is_local:
        try:
            with open(config.SERVER_CHAN_FILE, "r") as f:
                server_chan_key = f.read().strip()
        except:
            pass
    if server_chan_key:
        requests.post(config.SERVER_CHAN_SEND_URL.format(server_chan_key), data=data)


def main(is_local: bool):
    version = get_version()
    setup_logger(is_local)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logger.info(f"{'-' * 10}{now.center(len(now) + 2, ' ')}{'-' * 10}")
    logger.info(f"version: {version}")
    check_in = CheckInFactory.instance(is_local)
    result = check_in.process()
    remind_by_wechat(is_local, result)

    logger.info(f"{'-' * 10}{'end'.center(5, ' ')}{'-' * 10}\n")
    return result
