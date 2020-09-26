import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "_data")
LOG_FILE = os.path.join(DATA_DIR, "checkin.log")
LOG_FILE_MAX_SIZE = 5 * 1024 * 1024
LOG_FILE_BACKUP_COUNT = 5

USER_CONFIG_FILE = os.path.join(DATA_DIR, "user.config")
USER_COOKIES_FILE = os.path.join(DATA_DIR, "user.cookies")
PLATFORM_HOST = "https://www.deyun126.xyz"
LOGIN_SUCCESS_FLAG = 1
CHECK_IN_SUCCESS_FLAG = 1
