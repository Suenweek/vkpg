import os


# Common
BIN_DIR = "bin"
LOG_DIR = "log"


# WebDriver
GECKODRIVER_LOG_PATH = os.path.join(LOG_DIR, "geckodriver.log")
GECKODRIVER_EXECUTABLE_PATH = os.path.join(BIN_DIR, "geckodriver.exe")


# VK user credentials
VK_LOGIN = os.environ.get("VK_LOGIN")
VK_PASS = os.environ.get("VK_PASS")
