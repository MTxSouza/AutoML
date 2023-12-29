"""
Initializes all connections to MongoDB Server.
"""
from pymongo import MongoClient

ADMIN_USER = "admin"
ADMIN_PASSWORD = 1234
HOST="localhost"
PORT=80
CONNECTION_STRING = f"mongodb://{ADMIN_USER}:{ADMIN_PASSWORD}@{HOST}:{PORT}/"

mongo_client = MongoClient(
    host=CONNECTION_STRING
)

# creating database
db = mongo_client["automl_database"]

# creating collections
UserCollection = db["users"]
FileCollection = db["files"]
