#!/usr/bin/env python

import requests
import json
from urllib import parse
from datetime import datetime

PLATFROM_HOST = "https://www.deyun126.xyz"
USER_CONFIG_FILE = "user.config"
USER_COOKIES_FILE = "user.cookies"
LOGIN_SUCCESS_FLAG = "登录成功"


def get_local_user_info():
    with open(USER_CONFIG_FILE, "r") as cache_file:
        user_info = [x.strip() for x in cache_file.readlines()]
        if len(user_info) >= 2:
            return tuple(user_info[0:2])
        else:
            return None
    return None


def cache_cookies(cookies):
    cookies_dict = cookies.get_dict()
    with open(USER_COOKIES_FILE, "w+") as cache_file:
        cache_file.write(json.dumps(cookies_dict))
    return cookies_dict


def get_cookies():
    with open(USER_COOKIES_FILE, "r") as cache_file:
        content = cache_file.read()
        if not content:
            return None
        cookies = json.loads(content)
        expire_in = int(cookies["expire_in"])
        now = int(datetime.utcnow().timestamp())

        if now > expire_in:
            print("cookies expired!")
            return None
        else:
            print("use cache cookies.")
            return cookies

    return None


def login(user_info):
    username, password = user_info
    url = parse.urljoin(PLATFROM_HOST, "/auth/login")
    payload = {
        "email": username,
        "passwd": password,
        "code": ""
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    response = requests.post(url, headers=headers,
                             data=parse.urlencode(payload))

    if response.status_code == 200 and response.json()["msg"] == LOGIN_SUCCESS_FLAG:
        print("login successful")
        return cache_cookies(response.cookies)
    else:
        print("login failed")
        print(response.json())
        return None


def checkin(cookies):
    url = parse.urljoin(PLATFROM_HOST, "/user/checkin")
    headers = {
        'Accept': 'application/json'
    }
    response = requests.post(url, headers=headers, cookies=cookies)
    print(response.json())


def main():
    print(datetime.now())
    print("-"*20)
    cookies = get_cookies()
    if not cookies:
        user_info = get_local_user_info()
        if user_info:
            cookies = login(user_info)
        else:
            print("no user config, cat README.md")

    if cookies:
        checkin(cookies)

    print()


if __name__ == "__main__":
    main()
