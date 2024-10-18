import os
from pymongo import MongoClient

db_host = os.environ["DB_HOST"]
db_name = os.environ["DB_NAME"]

client = MongoClient(f'mongodb://{db_host}')
db = client[f'{db_name}']
collection = db['attributes']

def get_current_value(id):
  if type(id) == int:
    document = collection.findOne({"_id": id})
    return document['currentValue']
  else:
    return id