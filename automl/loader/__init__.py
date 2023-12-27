"""
Base class used to define file loaders.
"""
from abc import ABC, abstractmethod

import chardet
from fastapi import UploadFile


class FileLoader(ABC):
    def __init__(self) -> None:
        super(FileLoader, self).__init__()

        # attributes
        self.__file = None
        self.__mem_usg = 0
        self.__fname = None
        self.__enc = None

    # properties
    @property
    def file(self) -> bytes:
        return self.__file

    @file.setter
    def file(self, value: bytes) -> None:
        self.__file = value

    @property
    def memory_usage(self) -> int:
        return self.__mem_usg

    @memory_usage.setter
    def memory_usage(self, value: int) -> None:
        self.__mem_usg = value

    @property
    def filename(self) -> str | None:
        return self.__fname

    @filename.setter
    def filename(self, value: str) -> None:
        self.__fname = value

    @property
    def encoding(self) -> dict:
        return self.__enc

    @encoding.setter
    def encoding(self, value: dict) -> None:
        self.__enc = value

    # methods
    def find_encoding_mode(self, data: bytes | bytearray) -> dict:
        """
        Find the encoding mode of a file.
        """
        return chardet.detect(byte_str=data)

    def retrieve_content(self, file: UploadFile) -> None:
        """
        Retrieve all basic information about
        the file.
        """
        self.file = file.file.read()
        self.memory_usage = file.size
        self.filename = file.filename
        # finding encoding
        self.encoding = self.find_encoding_mode(data=self.file)
        file.file.close()

    @abstractmethod
    def load_file(self, file: UploadFile) -> dict:
        # retrieving file content
        self.retrieve_content(file=file)
