import base64
import json
import os
import sys
from os import path
import zipfile
from typing import Dict

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.scf.v20180416 import scf_client, models

sys.path.append(path.dirname(path.dirname(__file__)))

import config


def get_code():
    try:
        code_file = path.join(config.DATA_DIR, "code.zip")
        zipf = zipfile.ZipFile(code_file, "w", zipfile.ZIP_DEFLATED)
        zipf.write(path.join(config.ROOT_DIR, "run.py"), "run.py")
        zipf.write(path.join(config.ROOT_DIR, "config.py"), "config.py")
        zipf.write(path.join(config.ROOT_DIR, ".version"), ".version")

        src_dir = path.join(config.ROOT_DIR, "src")
        for file in os.listdir(src_dir):
            abspath = path.abspath(path.join(src_dir, file))
            if path.isfile(abspath) and path.splitext(file)[1] == ".py":
                zipf.write(path.join(src_dir, file), path.join("src", file))

        zipf.close()

        with open(code_file, "rb") as f:
            bytes = f.read()
            code_str = base64.b64encode(bytes).decode()
        os.unlink(code_file)
        return code_str
    except:
        return None


def get_secret_info():
    env_file = path.join(config.DATA_DIR, config.QCLOUD_ENV_FILE)
    try:
        with open(env_file, "r") as f:
            return dict([map(lambda x: x.strip(), line.strip().split("=")) for line in f.readlines()])
    except:
        return None


def set_version():
    stream = os.popen('git log --format="%h" -n 1')
    commit_id = stream.read().strip()
    try:
        with open(path.join(config.ROOT_DIR, ".version"), "w+") as f:
            f.write(commit_id)
    except:
        pass


def updateFunctionCode(secret_info: Dict[str, str], code: str):
    try:
        cred = credential.Credential(secret_info.get("TENCENT_SECRET_ID"), secret_info.get("TENCENT_SECRET_KEY"))
        httpProfile = HttpProfile()
        httpProfile.endpoint = config.QCLOUD_API_ENDPOINT

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = scf_client.ScfClient(cred, config.QCLOUD_REGION, clientProfile)

        req = models.UpdateFunctionCodeRequest()
        params = {
            "FunctionName": config.QCLOUD_FUNCTION_NAME,
            "Handler": config.QCLOUD_FUNCTION_HANDLER,
            "ZipFile": code
        }
        req.from_json_string(json.dumps(params))

        resp = client.UpdateFunctionCode(req)
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)


if __name__ == "__main__":
    set_version()
    secret_info = get_secret_info()
    code = get_code()
    if secret_info and code:
        updateFunctionCode(secret_info, code)
    else:
        if not code:
            print("no code")
        else:
            print("no secret_info")
