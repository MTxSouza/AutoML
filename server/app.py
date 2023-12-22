"""
Main script that initializes the server to
interact to the AutoML application.
"""
from fastapi import FastAPI

from server.routes.admin.router import router as admin_router
from server.routes.auth.router import router as auth_router
from server.routes.user.router import router as user_router

# creating API object
app = FastAPI()

# adding sub routes
app.include_router(router=auth_router)
app.include_router(router=admin_router)
app.include_router(router=user_router)


# main route
@app.route(path="/")
async def main():
    return {"AutoML": "running"}
