"""
Defines the MongoDB logger obejct to tracks
all interaction to database.
"""
import logging

# defining formatter
fmt = logging.Formatter(fmt="[%(levelname)-8s]: %(asctime)s - %(message)s (%(name)s)", datefmt="%d-%m-%Y %H:%M:%S")

# defining handler
hdlr = logging.FileHandler(filename="logs/database.log", mode="w", encoding="utf-8")
hdlr.setFormatter(fmt=fmt)

# defining logger
logger = logging.Logger(name="database")
logger.addHandler(hdlr=hdlr)
