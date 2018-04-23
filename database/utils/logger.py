import logging

class LoggerFactory:
    def __init__(self, filename, app_name="WeiboAnalysis"):
        self.logger = logging.getLogger(app_name)
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)

    def get_logger(self, level=logging.DEBUG):
        self.logger.setLevel(level)
        return self.logger

