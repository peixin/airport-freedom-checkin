import os
from typing import Dict

from src import main


def main_handler(event: Dict, context: Dict):
    is_cloud_function = os.environ.get("TENCENTCLOUD_RUNENV") is not None
    main(not is_cloud_function)


if __name__ == "__main__":
    main_handler(None, None)
