import sys
from os import path
from typing import Dict
import json
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.scf.v20180416 import models

sys.path.append(path.dirname(path.dirname(__file__)))
import config
from deploy.qcloud_scf_common import get_secret_info, get_scf_client


def create_trigger(secret_info: Dict[str, str]):
    try:
        client = get_scf_client(secret_info)

        req = models.CreateTriggerRequest()
        params = {
            "FunctionName": config.QCLOUD_FUNCTION_NAME,
            "TriggerName": "checkin-trigger",
            "Type": "timer",
            "TriggerDesc": "0 0 4 * * * *",
            "Enable": "OPEN"
        }
        req.from_json_string(json.dumps(params))

        resp = client.CreateTrigger(req)
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)


def main():
    secret_info = get_secret_info()
    if secret_info:
        create_trigger(secret_info)
    else:
        print("no secret_info")


if __name__ == "__main__":
    main()
