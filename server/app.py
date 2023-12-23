"""
Main script that initializes the server to
interact to the AutoML application.
"""
from fastapi import FastAPI

from server.routes.admin.router import router as admin_router
from server.routes.auth.router import router as auth_router
from server.routes.user.router import router as user_router
from server.logging import logger

# creating API object
logger.trace(msg="Initializing FastAPI object")
app = FastAPI()

# adding sub routes
logger.trace(msg="Including sub-routes")
app.include_router(router=auth_router)
app.include_router(router=admin_router)
app.include_router(router=user_router)


# main route
logger.trace(msg="Creating main API route")
@app.get(path="/")
async def main():
    return {"AutoML": "running"}

logger.info(msg="Server is running")
