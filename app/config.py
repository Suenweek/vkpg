import os


# Common
APP_NAME = "VKPG"
SECRET_KEY = os.environ.get("VKPG_SECRET_KEY")
DEBUG = os.environ.get("VKPG_DEBUG")
LOG_DIR = "log"
IMG_DIR = "img"


# VK
VK_API_VERSION = "5.8"
VK_CONSUMER_KEY = os.environ.get("VKPG_VK_CONSUMER_KEY", "")
VK_CONSUMER_SECRET = os.environ.get("VKPG_VK_CONSUMER_SECRET", "")
VK_PERMISSIONS = ""
