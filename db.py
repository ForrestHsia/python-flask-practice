import pymongo


def db_init():
    mongoCon = "localhost:27017"
    client = pymongo.MongoClient(mongoCon)
    return client
