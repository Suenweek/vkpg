import os
import sys


# General
APP_NAME = "VKPG"

# Dirs
BASEDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
LOG_DIR = "log"
IMG_DIR = "img"

# Secret key
SECRET_KEY = os.environ.get("VKPG_SECRET_KEY")

# Debug
DEBUG = os.environ.get("VKPG_DEBUG")

# VK
VK_API_VERSION = "5.8"
VK_CONSUMER_KEY = os.environ.get("VKPG_VK_CONSUMER_KEY", "")
VK_CONSUMER_SECRET = os.environ.get("VKPG_VK_CONSUMER_SECRET", "")
VK_PERMISSIONS = ""
