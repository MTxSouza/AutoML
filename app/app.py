"""
Initializes the API of AutoML application.
"""
from typing import Annotated

from fastapi import Depends, FastAPI, status
from fastapi.responses import RedirectResponse
from pymongo.database import Database

from app.admin.router import router as admin_router
from app.logging import logger as api_logger
from database.utils import get_db

app = FastAPI()
app.include_router(router=admin_router)


@app.get(path="/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def config(db: Annotated[Database, Depends(dependency=get_db)]):
    api_logger.debug(msg="/ has been called. Redirecting to /automl")
    return RedirectResponse(url="/automl")


@app.get(path="/automl", response_model=dict, status_code=status.HTTP_200_OK)
async def automl():
    api_logger.debug(msg="/automl has been called")
    return {"name": "AutoML", "status": "Running"}
