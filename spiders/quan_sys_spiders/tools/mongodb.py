import pymongo

class MongoInstance(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    
    def find(self, collection, query, field):
        result = self.db[collection].find(query, field)
        return result

    def findOne(self, collection, query, field):
        result = self.db[collection].find_one(query, field)
        return result

    def close(self):
        self.client.close()

if __name__ == "__main__":
    db = MongoInstance('localhost', 'stock')
    result = db.find('stock', {}, {'_id': 0, 'code': 1})
    for item in result:
        print(item['code'])
    