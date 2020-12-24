from typing import Tuple, Dict, Union
import abc
import requests
import json
from urllib import parse
from datetime import datetime
import os

import config
from .logger import logger


def parse_json(text: str):
    try:
        return json.loads(text)
    except:
        return None


class CheckIn(metaclass=abc.ABCMeta):
    PLATFORM_HOST = config.PLATFORM_HOST
    LOGIN_SUCCESS_FLAG = config.LOGIN_SUCCESS_FLAG
    CHECK_IN_SUCCESS_FLAG = config.CHECK_IN_SUCCESS_FLAG

    def __init__(self) -> None:
        super().__init__()
        self.user_info: Tuple[str, str] = None
        self.cookies: Dict[str, Union[str, int]] = None

    @abc.abstractmethod
    def init_user_info(self) -> None:
        pass

    def login(self) -> None:
        if not self.user_info:
            logger.error("no user info")
            return
        username, password = self.user_info

        url = parse.urljoin(CheckIn.PLATFORM_HOST, "/auth/login")
        payload = {"email": username, "passwd": password, "code": ""}
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

        response = requests.post(url, headers=headers, data=parse.urlencode(payload))

        data = parse_json(response.text)
        if (
            response.status_code == 200
            and data
            and data.get("ret") == CheckIn.LOGIN_SUCCESS_FLAG
        ):
            logger.info("login successful")
            self.cookies = response.cookies.get_dict()
            return

        logger.error("login failed")
        logger.error(response.text)

    def check_in(self) -> Tuple[bool, str, str]:
        if not self.cookies:
            logger.warn("no cookies")
            return
        url = parse.urljoin(CheckIn.PLATFORM_HOST, "/user/checkin")
        headers = {"Accept": "application/json"}
        response = requests.post(url, headers=headers, cookies=self.cookies)
        data = parse_json(response.text)
        if data:
            traffic_info = ""
            if data.get("ret", 0) == CheckIn.CHECK_IN_SUCCESS_FLAG:
                logger.info("check in successful")
                logger.info(data.get("msg", "no message"))
                logger.info(data.get("trafficInfo"))
                traffic_info = data.get("trafficInfo", {})
                traffic_info = f"```{traffic_info}```"
            else:
                logger.info(data.get("msg", "no message"))
            return True, data.get("msg", "no message"), traffic_info
        else:
            logger.error("check in failed")
            logger.error(response.text)
            text = response.text.strip()
            if text.startswith("<!DOCTYPE html>"):
                text = "raw html"
            return False, "Check In Failed", text

    @abc.abstractmethod
    def cache_cookies(self) -> None:
        pass

    def process(self):
        self.init_user_info()
        self.login()
        self.cache_cookies()
        return self.check_in()


class CheckInLocal(CheckIn):
    USER_CONFIG_FILE = config.USER_CONFIG_FILE
    USER_COOKIES_FILE = config.USER_COOKIES_FILE

    def init_user_info(self):
        with open(CheckInLocal.USER_CONFIG_FILE, "r") as cache_file:
            user_info = [x.strip() for x in cache_file.readlines()]
            if len(user_info) >= 2:
                self.user_info = tuple(user_info[0:2])

    def get_cookies(self):
        if not os.path.exists(CheckInLocal.USER_COOKIES_FILE):
            return
        with open(CheckInLocal.USER_COOKIES_FILE, "r") as cache_file:
            content = cache_file.read()
            cookies = parse_json(content)
            if not cookies:
                return
            expire_in = int(cookies.get("expire_in", 0))
            now = int(datetime.utcnow().timestamp())

            if now > expire_in:
                logger.info("cookies expired!")
            else:
                logger.info("use cache cookies.")
                self.cookies = cookies

    def login(self):
        self.get_cookies()
        if not self.cookies:
            super(CheckInLocal, self).login()

    def cache_cookies(self):
        if not self.cookies:
            return
        with open(CheckInLocal.USER_COOKIES_FILE, "w+") as cache_file:
            cache_file.write(json.dumps(self.cookies))


class CheckInSCF(CheckIn):
    def init_user_info(self):
        username = os.environ.get("USERNAME", "")
        password = os.environ.get("PASSWORD", "")
        if username and password:
            self.user_info = username, password

    def cache_cookies(self) -> None:
        pass


class CheckInFactory(object):
    @staticmethod
    def instance(is_local: bool) -> CheckIn:
        if is_local:
            return CheckInLocal()
        else:
            return CheckInSCF()
