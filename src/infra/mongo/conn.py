import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["chat-users"]

mydb.list_collection_names()
