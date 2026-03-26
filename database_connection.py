import pprint

from bson import ObjectId
import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import encryption


def connect_db():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        database = client['prodKoMeat']  # You can use any existing database here
        print("Connection to MongoDB established.")
        return database
    except ConnectionFailure:
        print("Failed to connect to MongoDB.")


# Get all batches from batches collection
def getBatches(database):
    batches_collection = database['batches']
    return batches_collection.find({}).limit(3)  # Retrieve the first two documents in the collection


# Store the local block to blockchain collection
def storeBlock(database, block):
    if 'blockchain' not in database.list_collection_names():
        print('Creating blockchain collection...')
        database.create_collection('blockchain')
    database['blockchain'].insert_one(block)


# Return record - block from blockchain collection based on batch Number
def batchNumberToHash(database, batchNumber):
    batchesList = list(database['blockchain'].find({"data_type": "main_info"}))
    for batch in batchesList:
        if encryption.decrypt_data(encryption.generate_encyption_key(), batch['data'])['batchNumber'] == batchNumber:
            return batch


# Returns the latest record - block in blockchain collection
def getLatestBlock(database):
    return database['blockchain'].find().sort([('_id', -1)]).limit(1).next()


# Recursively converts ObjectId and datetime.datetime objects to strings within a dictionary or list.
def convert_to_strings(document):
    if isinstance(document, dict):
        for key, value in document.items():
            if isinstance(value, ObjectId):
                document[key] = str(value)
            elif isinstance(value, datetime.datetime):
                document[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, (dict, list)):
                convert_to_strings(value)
    elif isinstance(document, list):
        for i, item in enumerate(document):
            if isinstance(item, ObjectId):
                document[i] = str(item)
            elif isinstance(item, datetime.datetime):
                document[i] = item.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(item, (dict, list)):
                convert_to_strings(item)
