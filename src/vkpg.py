import logging
import requests
from functools import partial
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from tqdm import tqdm
from . import config, selectors


VK_URL = "https://vk.com"
FEW_SECONDS = 5


class VkAlbumGetter(object):
    """
    Allows to download photo albums from vk
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver = webdriver.Firefox(
            log_path=config.GECKODRIVER_LOG_PATH,
            executable_path=config.GECKODRIVER_EXECUTABLE_PATH
        )
        self.wait = partial(WebDriverWait, self.driver)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.driver.quit()

    def login(self):
        # Proceeding to login page
        self.driver.get(VK_URL)

        # Finding login form
        self.wait(FEW_SECONDS).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, selectors.FORM_LOGIN))
        )

        # Filling out login input
        input_login = self.driver.find_element_by_css_selector(selectors.INPUT_LOGIN)
        input_login.clear()
        input_login.send_keys(config.VK_LOGIN)

        # Filling out password input
        input_pass = self.driver.find_element_by_css_selector(selectors.INPUT_PASS)
        input_pass.clear()
        input_pass.send_keys(config.VK_PASS)

        # Submitting the form
        button_login = self.driver.find_element_by_css_selector(selectors.BTN_LOGIN)
        button_login.click()

        # Checking if login succeeded
        self.wait(FEW_SECONDS).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, selectors.PROFILE_NAME))
        )

    def get_album(self, first_photo_url):
        self.driver.get(first_photo_url)
        pass


class Photo(object):
    """
    Represents a photo
    """
    def __init__(self):
        pass

    @property
    def url(self):
        raise NotImplementedError
        # return self.url

    @property
    def raw(self):
        raise NotImplementedError
        # return self.raw
