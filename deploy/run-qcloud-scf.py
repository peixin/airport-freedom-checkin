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


def run_function(secret_info: Dict[str, str]):
    try:
        client = get_scf_client(secret_info)
        req = models.InvokeRequest()
        params = {
            "FunctionName": config.QCLOUD_FUNCTION_NAME,
            "LogType": "None",
        }
        req.from_json_string(json.dumps(params))

        resp = client.Invoke(req)
        response_json = json.loads(resp.to_json_string())
        response_json["Result"]["RetMsg"] = json.loads(
            response_json["Result"]["RetMsg"]
        )
        response_json = json.dumps(response_json, indent=2, ensure_ascii=False)
        print(response_json)
    except TencentCloudSDKException as err:
        print(err)


def main():
    secret_info = get_secret_info()
    if secret_info:
        run_function(secret_info)
    else:
        print("no secret_info")


if __name__ == "__main__":
    main()
