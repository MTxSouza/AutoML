"""
Initializes all connections to MongoDB Server.
"""
from database.logging import logger

from pymongo.errors import ServerSelectionTimeoutError
from pymongo import MongoClient

import sys

ADMIN_USER = "admin"
ADMIN_PASSWORD = 1234
HOST = "localhost"
PORT = 80
MS_TIMEOUT = 10000
CONNECTION_STRING = f"mongodb://{ADMIN_USER}:{ADMIN_PASSWORD}@{HOST}:{PORT}/"

mongo_client = MongoClient(host=CONNECTION_STRING, serverSelectionTimeoutMS=MS_TIMEOUT)
logger.debug(msg="MongoDB client has been created")

# creating database
db = mongo_client["automl_database"]
logger.debug(msg="`automl_database` database has been defined")

# creating collections
UserCollection = db["users"]
logger.debug(msg="`users` collection has been defined")
FileCollection = db["files"]
logger.debug(msg="`files` collection has been defined")

# checking connection
logger.debug(msg="Checking MongoDB connection")
try:
    db.list_collection_names()
except ServerSelectionTimeoutError:
    logger.critical(msg="Could not connect to MongoDB Server")
    sys.exit(1)
logger.info(msg="MongoDB Server is running")
