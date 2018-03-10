from logger import LoggerFactory
from database.setup import PATH_TO_LOG
from os import path

scrape_logger = LoggerFactory('weibo_scrape', path.join(PATH_TO_LOG, 'scrape_log.txt')).get_logger()