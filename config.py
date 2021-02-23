import os

ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, "_data")
TIMEZONE = "Asia/Shanghai"

# check in
LOG_FILE = os.path.join(DATA_DIR, "checkin.log")
LOG_FILE_MAX_SIZE = 5 * 1024 * 1024
LOG_FILE_BACKUP_COUNT = 5

USER_CONFIG_FILE = os.path.join(DATA_DIR, "user.config")
USER_COOKIES_FILE = os.path.join(DATA_DIR, "user.cookies")
PLATFORM_HOST = "https://www.deyun128.xyz"  # your jichang url
LOGIN_SUCCESS_FLAG = 1
CHECK_IN_SUCCESS_FLAG = 1

# deploy
QCLOUD_ENV_FILE = os.path.join(DATA_DIR, "qcloud.env")
QCLOUD_API_ENDPOINT = "scf.tencentcloudapi.com"
QCLOUD_REGION = "ap-guangzhou"
QCLOUD_FUNCTION_NAME = "freedom-checkin"  # your scf function name
QCLOUD_FUNCTION_NAME_TRIGGER = "0 0 5 * * * *"  # your trigger crontab
QCLOUD_FUNCTION_HANDLER = "run.main_handler"

# remind wechat
SERVER_CHAN_FILE = os.path.join(DATA_DIR, "server-chan-key")
SERVER_CHAN_SEND_URL = "https://sctapi.ftqq.com/{}.send"
