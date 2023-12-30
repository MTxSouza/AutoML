"""
Initializes all connections to MongoDB Server.
"""
from motor.motor_asyncio import AsyncIOMotorClient

from database.logging import logger as db_logger

ADMIN_USER = "admin"
ADMIN_PASSWORD = 1234
HOST = "localhost"
PORT = 80
MS_TIMEOUT = 10000
CONNECTION_STRING = f"mongodb://{ADMIN_USER}:{ADMIN_PASSWORD}@{HOST}:{PORT}/"

# checking connection
mongo_client = AsyncIOMotorClient(
    host=CONNECTION_STRING, serverSelectionTimeoutMS=MS_TIMEOUT
)
db_logger.debug(msg="MongoDB client has been created")

# creating database
db = mongo_client.get_database(name="auto_database")
db_logger.debug(msg="`automl_database` database has been defined")
db_logger.info(msg=f"MongoDB Server is running")
