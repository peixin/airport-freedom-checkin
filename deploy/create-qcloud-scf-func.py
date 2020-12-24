import sys
from os import path
from typing import Dict
import json
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.scf.v20180416 import models

sys.path.append(path.dirname(path.dirname(__file__)))
import config
from deploy.qcloud_scf_common import (
    get_secret_info,
    set_version,
    get_code,
    get_scf_client,
)


def create_function(secret_info: Dict[str, str], code: str, envs: Dict):
    try:
        client = get_scf_client(secret_info)

        req = models.CreateFunctionRequest()
        params = {
            "FunctionName": config.QCLOUD_FUNCTION_NAME,
            "Handler": config.QCLOUD_FUNCTION_HANDLER,
            "Description": "for freedom check in function",
            "Code": {"ZipFile": code},
            "MemorySize": 128,
            "Timeout": 30,
            "Environment": {
                "Variables": [
                    {"Key": "USERNAME", "Value": envs.get("user_info")[0]},
                    {"Key": "PASSWORD", "Value": envs.get("user_info")[1]},
                    {"Key": "SERVER_CHAN_KEY", "Value": envs.get("server_chan_key")},
                ]
            },
            "Runtime": "Python3.6",
        }
        req.from_json_string(json.dumps(params))

        resp = client.CreateFunction(req)
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)


def get_envs():
    user_info = None
    with open(config.USER_CONFIG_FILE, "r") as cache_file:
        _user_info = [x.strip() for x in cache_file.readlines()]
        if len(_user_info) >= 2:
            user_info = tuple(_user_info[0:2])

    with open(config.SERVER_CHAN_FILE, "r") as f:
        server_chan_key = f.read().strip()

    if user_info is None or server_chan_key is None:
        return None

    return {
        "user_info": user_info,
        "server_chan_key": server_chan_key,
    }


def main():
    set_version()
    envs = get_envs()
    secret_info = get_secret_info()
    code = get_code()
    if secret_info and code and envs:
        create_function(secret_info, code, envs)
    else:
        if not code:
            print("no code")
        elif not envs:
            print("no envs")
        else:
            print("no secret_info")


if __name__ == "__main__":
    main()
