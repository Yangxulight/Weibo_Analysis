import os

PATH_TO_DATABASE = os.getcwd()
PATH_TO_PROJECT = os.path.abspath(os.path.join(PATH_TO_DATABASE, os.pardir))
COOKIE_FILE_NAME = "cookies.ini"
PATH_TO_LOG = os.path.join(PATH_TO_DATABASE, 'log')
PATH_TO_LOCAL_DATA = os.path.join(PATH_TO_DATABASE, 'cache')
PATH_TO_MONGODB = os.path.join(PATH_TO_DATABASE, 'data')