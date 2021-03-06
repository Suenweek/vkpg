import os
import sys


# General
APP_NAME = "vkpg"
REPO_URL = "https://github.com/Suenweek/vkpg"
BASEDIR = os.path.abspath(os.path.dirname(sys.argv[0]))

# Secret key
SECRET_KEY = os.environ.get("VKPG_SECRET_KEY", "You'd better set it yourself")

# Debug
DEBUG = os.environ.get("VKPG_DEBUG")

# Logging
LOG_DIR = os.path.join(BASEDIR, "log")
LOG_PATH = os.path.join(LOG_DIR, "%s.log" % APP_NAME)
LOG_FMT = "%(asctime)s %(levelname)s - %(message)s"
LOG_MAX_BYTES = 1024 * 1024 * 10  # 10 MB
LOG_BAK_COUNT = 3

# VK
VK_API_VERSION = "5.69"
VK_CONSUMER_KEY = os.environ.get("VKPG_VK_CONSUMER_KEY")
VK_CONSUMER_SECRET = os.environ.get("VKPG_VK_CONSUMER_SECRET")
VK_APP_PARAMS_SET = not (VK_CONSUMER_KEY is None or VK_CONSUMER_SECRET is None)
VK_PERMISSIONS = "photos"
