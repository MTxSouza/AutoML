"""
Initializes all connections to MongoDB Server.
"""
import asyncio
import sys

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import CollectionInvalid, ServerSelectionTimeoutError

from database.logging import logger

ADMIN_USER = "admin"
ADMIN_PASSWORD = 1234
HOST = "localhost"
PORT = 80
MS_TIMEOUT = 10000
CONNECTION_STRING = f"mongodb://{ADMIN_USER}:{ADMIN_PASSWORD}@{HOST}:{PORT}/"

try:
    # checking connection
    mongo_client = AsyncIOMotorClient(
        host=CONNECTION_STRING, serverSelectionTimeoutMS=MS_TIMEOUT
    )
    logger.debug(msg="MongoDB client has been created")

    # creating database
    db = mongo_client.get_database(name="auto_database")
    logger.debug(msg="`automl_database` database has been defined")
    collection_names = ["users", "files"]

    # creating collections
    async def create_collections() -> None:
        for name in collection_names:
            await db.create_collection(name=name)
            logger.debug(msg=f"`{name}` collection has been defined")
        # filtering collections
        if not all(col in collection_names for col in await db.list_collection_names()):
            raise RuntimeError()

    # checking collections
    async def check_collections() -> None:
        for name in collection_names:
            await db.validate_collection(name_or_collection=name)
            logger.debug(msg=f"`{name}` collection has been validated")

    # run async
    async def main() -> None:
        task1 = asyncio.create_task(coro=create_collections())
        await task1

        task2 = asyncio.create_task(coro=check_collections())
        await task2

    asyncio.run(main=main())

except ServerSelectionTimeoutError:
    logger.critical(msg="Could not connect to MongoDB Server")
    sys.exit(0)
except RuntimeError as error:
    print(error)
    logger.critical(msg="Missing collections in database")
    sys.exit(0)
except CollectionInvalid:
    logger.critical(msg="Could validate the collections correctly")
    sys.exit(0)
logger.info(msg=f"MongoDB Server is running")
