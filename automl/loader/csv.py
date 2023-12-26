"""
Main class to handle any .csv file.
"""
import io
import json

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
                    df = pd.read_csv(
                        buffer, sep=sep, encoding=self.encoding["encoding"]
                    )
                    assert df.shape[1] != 1
            except Exception as error:
                logger.error(msg=str(error))
                continue
            logger.debug(msg="Possible separator for CSV file has been found")
            available_separators.append(sep)
        if available_separators:
            return {
                "file": json.dumps(obj=df.to_json(force_ascii=False)),
                "filename": self.filename,
                "separator": str(available_separators),
                "encoding": self.encoding["encoding"],
                "size": self.memory_usage,
            }
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not convert the CSV file into a table",
        )
