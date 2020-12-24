import json
import sys
from os import path
from typing import Dict
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


def update_function_code(secret_info: Dict[str, str], code: str):
    try:
        client = get_scf_client(secret_info)

        req = models.UpdateFunctionCodeRequest()
        params = {
            "FunctionName": config.QCLOUD_FUNCTION_NAME,
            "Handler": config.QCLOUD_FUNCTION_HANDLER,
            "ZipFile": code,
        }
        req.from_json_string(json.dumps(params))

        resp = client.UpdateFunctionCode(req)
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)


def main():
    set_version()
    secret_info = get_secret_info()
    code = get_code()
    if secret_info and code:
        update_function_code(secret_info, code)
    else:
        if not code:
            print("no code")
        else:
            print("no secret_info")


if __name__ == "__main__":
    main()
