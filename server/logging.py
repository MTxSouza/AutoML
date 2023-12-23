"""
File that contains the logger object used to
track all traffic in API.
"""
from logging import Logger, FileHandler, Formatter

# defining formatter
fmt = Formatter(fmt="[%(levelname)-8s] - %(asctime)s - %(message)s")

# defining handler
hdlr = FileHandler(filename="automl.log", mode="w", encoding="utf-8")
hdlr.setFormatter(fmt=fmt)

# defining logger
logger = Logger(name="automl_logger")
logger.addHandler(hdlr=hdlr)
