from pymongo import MongoClient

class MongoDB:
    def __init__(self, host="localhost", port=27017):
        self.host = host
        self.port = port
        self.client = MongoClient('{}:{}'.format(host, port))
        
    def save_document(self, collection="weibo", db_name="weibo_database", data):
        db_collection = self.dispatch(collection, db_name)
        if type(data) == list:
            db_collection.insert_many(data)
        else:
            db_collection.insert_one(data)

    def dispatch(self, collection, db_name):
        return self.client[db_name][collection]

    def query(self, collection, db_name="weibo_database", condition = ""):
        db_collection = self.dispatch(collection, db_name)
        result_list = []
        if condition == "":
            # return all documents
            for item in db_collection.find():
                result_list.append(item)
        else:
            for item in db_collection.find(condition):
                result_list.append(item)
        return result_list

