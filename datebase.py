from pymongo import MongoClient
from config.config import MONGODB_SETTINGS

client = MongoClient(MONGODB_SETTINGS['host'], MONGODB_SETTINGS['port'])
db = client[MONGODB_SETTINGS['db']]