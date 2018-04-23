from utils.logger import LoggerFactory
from os import path
import os

CURRENT_PATH = os.getcwd()
PATH_TO_LOG = path.join(CURRENT_PATH, 'log')
scrape_logger = LoggerFactory(filename=path.join(PATH_TO_LOG, 'scrape_log.txt'), app_name='weibo_scrape').get_logger()