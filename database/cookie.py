from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from setup import PATH_TO_DATABASE, PATH_TO_PROJECT, COOKIE_FILE_NAME
from os import path
import pickle
from utils.scrape_logger import scrape_logger as logger

class Cookie:
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url
        self.file_name = COOKIE_FILE_NAME
    
    def save_cookeis(self):
        logger.debug("saving cookies.")
        driver = webdriver.Chrome()
        driver.get(self.url)
        login_button = driver.find_element_by_class_name("ut").find_element_by_tag_name('a')[0]
        login_button.click()
        username_input = driver.find_element_by_id('loginName')
        password_input = driver.find_element_by_id('loginPassword')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        cookie = driver.get_cookies()
        pickle.dump(cookie, open(path.join(PATH_TO_DATABASE, self.file_name), "wb"))

    @staticmethod
    def load_cookies():
        logger.debug("loading cookies.")
        return pickle.load(open(path.join(PATH_TO_DATABASE, COOKIE_FILE_NAME),"rb"))


