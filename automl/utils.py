"""
Basic functions to be used in whole
package.
"""
from typing import BinaryIO

import pandas as pd
from fastapi import status
from fastapi.exceptions import HTTPException


def check_file_content(file_buffer: BinaryIO, content_type: str) -> dict | None:
    """
    Check file content including its extension.
    """
    # mapper
    available_files = {"csv": load_csv_file}
    # checking extension
    ext = content_type.split(sep="/")[1]
    if not ext in available_files:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid file format"
        )
    # loading file
    return available_files[ext](file_buffer=file_buffer)


def find_encoding_mode(data: bytes | bytearray) -> list[str]:
    """
    Find the encoding mode of a file.
    """
    available_encodes = [
        "ascii",
        "big5",
        "big5hkscs",
        "cp037",
        "cp273",
        "cp424",
        "cp437",
        "cp500",
        "cp720",
        "cp737",
        "cp775",
        "cp850",
        "cp852",
        "cp855",
        "cp856",
        "cp857",
        "cp858",
        "cp860",
        "cp861",
        "cp862",
        "cp863",
        "cp864",
        "cp865",
        "cp866",
        "cp869",
        "cp874",
        "cp875",
        "cp932",
        "cp949",
        "cp950",
        "cp1006",
        "cp1026",
        "cp1125",
        "cp1140",
        "cp1250",
        "cp1251",
        "cp1252",
        "cp1253",
        "cp1254",
        "cp1255",
        "cp1256",
        "cp1257",
        "cp1258",
        "euc_jp",
        "euc_jis_2004",
        "euc_jisx0213",
        "euc_kr",
        "gb2312",
        "gbk",
        "gb18030",
        "hz",
        "iso2022_jp",
        "iso2022_jp_1",
        "iso2022_jp_2",
        "iso2022_jp_2004",
        "iso2022_jp_3",
        "iso2022_jp_ext",
        "iso2022_kr",
        "latin_1",
        "iso8859_2",
        "iso8859_3",
        "iso8859_4",
        "iso8859_5",
        "iso8859_6",
        "iso8859_7",
        "iso8859_8",
        "iso8859_9",
        "iso8859_10",
        "iso8859_11",
        "iso8859_13",
        "iso8859_14",
        "iso8859_15",
        "iso8859_16",
        "johab",
        "koi8_r",
        "koi8_t",
        "koi8_u",
        "kz1048",
        "mac_cyrillic",
        "mac_greek",
        "mac_iceland",
        "mac_latin2",
        "mac_roman",
        "mac_turkish",
        "ptcp154",
        "shift_jis",
        "shift_jis_2004",
        "shift_jisx0213",
        "utf_32",
        "utf_32_be",
        "utf_32_le",
        "utf_16",
        "utf_16_be",
        "utf_16_le",
        "utf_7",
        "utf_8",
        "utf_8_sig",
    ]

    encode_list = []
    for encoding in available_encodes:
        try:
            data.decode(encoding=encoding)
        except UnicodeDecodeError:
            continue
        else:
            encode_list.append(encoding)
    if encode_list:
        return encode_list
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Could not find the decode mode of file",
    )


def load_csv_file(file_buffer: BinaryIO) -> dict:
    """
    Load any .csv file.
    """
    # loading file
    df = pd.read_csv(filepath_or_buffer=file_buffer)
    df_sample = df.head(n=100).values.tobytes()
    # checking memory size
    mb = df.memory_usage(deep=True).sum().item()
    # checking number of registers
    registers = df.shape[0]
    # checking fields
    fields = list(df.columns)
    # finding decode mode
    data_bytes = df.values.tobytes()
    encoding_list = find_encoding_mode(data=data_bytes)
    encoding = encoding_list[0]
    return {
        "file": {
            "sample": df_sample.decode(encoding=encoding),
            "registers": registers,
            "fields": fields,
        },
        "encoding_list": encoding_list,
        "encoding": encoding,
        "mb": mb,
    }
