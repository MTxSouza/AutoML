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
        str_content = self.file.decode(encoding=self.encoding["encoding"]).strip()
        # loading table
        base_table = str_content.split(sep="\n")
        available_separators = []
        # finding all available characters
        for sep in self.__separators:
            # creating table
            table = list(map(lambda row: row.split(sep=sep), base_table))
            # checking consistent shape
            try:
                np_table = np.asarray(a=table)
                assert np_table.shape[1] != 1
                del np_table
            except Exception:
                continue
            # creating dataframe
            try:
                buffer = io.StringIO(initial_value=str_content)
                df = pd.read_csv(buffer, sep=sep, encoding=self.encoding["encoding"])
            except Exception as error:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
                )
            finally:
                buffer.close()
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
