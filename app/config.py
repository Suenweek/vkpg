import os
import sys


# General
APP_NAME = "VKPG"

# Dirs
BASEDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
TMP_DIR = os.path.join(BASEDIR, "tmp")
LOG_DIR = os.path.join(TMP_DIR, "log")
ALBUMS_DIR = os.path.join(TMP_DIR, "albums")

# Secret key
SECRET_KEY = os.environ.get("VKPG_SECRET_KEY")

# Debug
DEBUG = os.environ.get("VKPG_DEBUG")

# VK
VK_API_VERSION = "5.69"
VK_CONSUMER_KEY = os.environ.get("VKPG_VK_CONSUMER_KEY", "")
VK_CONSUMER_SECRET = os.environ.get("VKPG_VK_CONSUMER_SECRET", "")
VK_PERMISSIONS = "photos"
