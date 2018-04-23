from pymongo import MongoClient
from utils.scrape_logger import scrape_logger as logger

class MongoDB:
    def __init__(self, host="localhost", port=27017):
        self.host = host
        self.port = port
        logger.debug("connecting to mongodb at {}:{}".format(host, port))
        self.client = MongoClient('{}:{}'.format(host, port))
        
    def save_document(self, data, collection="weibo", db_name="weibo_database"):
        logger.debug("saving document to condition:{}".format(collection))
        db_collection = self.dispatch(collection, db_name)
        if type(data) == list:
            db_collection.insert_many(data)
        else:
            db_collection.insert_one(data)

    def dispatch(self, collection, db_name):
        return self.client[db_name][collection]

    def query(self, collection, db_name="weibo_database", condition = {}):
        logger.debug("query from collection:{} with condition{}".format(collection, condition))
        db_collection = self.dispatch(collection, db_name)
        result_list = []
        if condition == {}:
            # return all documents
            for item in db_collection.find():
                result_list.append(item)
        else:
            for item in db_collection.find(condition):
                result_list.append(item)
        return result_list

