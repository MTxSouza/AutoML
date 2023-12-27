"""
Basic functions to be used in whole
package.
"""
from fastapi import UploadFile, status
from fastapi.exceptions import HTTPException

from automl.loader.csv import CSVLoader


def check_file_content(file: UploadFile) -> dict:
    """
    Check file content including its extension.
    """
    # checking size
    if file.size > int(1024**2 * 10):
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Files larger than 10mb is not allowed, this file has {file.size}",
        )
    # mapper
    available_files = {"csv": CSVLoader}
    # checking extension
    ext = file.content_type.split(sep="/")[1]
    if not ext in available_files:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Invalid file format",
        )
    # loading file
    loader = available_files[ext]()
    return loader.load_file(file=file)
