"""
Main class to handle any .csv file.
"""
import io
import json

import numpy as np
import pandas as pd
from fastapi import UploadFile, status
from fastapi.exceptions import HTTPException

from automl.loader import FileLoader
from server.logging import logger


class CSVLoader(FileLoader):
    def __init__(self) -> None:
        super(CSVLoader, self).__init__()

        # properties
        self.__cols = []

        # variables
        self.__separators = [
            ",",
            ";",
            "~",
            "^",
            "!",
            "@",
            "#",
            "$",
            "%",
            "&",
            "|",
            "´",
            "`",
            ".",
            "-",
            "_",
            "+",
            "=",
        ]
        logger.debug(msg="Initializing CSV loader")

    # properties
    @property
    def columns(self) -> list:
        return self.__cols

    @columns.setter
    def columns(self, value: list) -> None:
        self.__cols = value

    # methods
    def load_file(self, file: UploadFile) -> dict:
        super().load_file(file)
        # converting to string
        logger.debug(msg="Looking for CSV file encoding")
        str_content = self.file.decode(encoding=self.encoding["encoding"]).strip()
        # finding all available separators
        logger.debug(msg="Looking for CSV separator")
        available_separators = []
        for sep in self.__separators:
            # creating dataframe
            try:
                with io.StringIO(initial_value=str_content) as buffer:
                    df = pd.read_csv(buffer, sep=sep, encoding=self.encoding["encoding"])
                    assert df.shape[1] != 1
            except Exception as error:
                logger.error(msg=str(error))
                continue
            logger.debug(msg="Possible separator for CSV file has been found")
            # retriving columns
            self.columns = list(df.columns)
            # making preview
            preview_table = json.loads(s=df.head(n=5).to_json(orient="records"))
            available_separators.append(
                {
                    "separator": sep,
                    "shape": df.shape,
                    "columns": self.columns,
                    "content": preview_table,
                }
            )
        if available_separators:
            return {
                "data": {
                    "previews": available_separators,
                    "memory": self.memory_usage,
                },
                "filename": self.filename,
                "encoding": self.encoding,
            }
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not convert the CSV file into a table",
        )
