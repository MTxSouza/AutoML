"""
File that contains the logger object used to
track all traffic in API.
"""
from logging import Logger, FileHandler, Formatter
import logging

# defining formatter
fmt = Formatter(fmt="[%(levelname)-8s] - %(asctime)s - %(message)s")

# defining handler
hdlr = FileHandler(filename="automl.log", mode="w", encoding="utf-8")
hdlr.setFormatter(fmt=fmt)

# creating trace level
__trace_id = 9
def trace(self, msg, *args, **kargs):
    if self.isEnabledFor(__trace_id):
        self._log(__trace_id, msg, args, **kargs)
logging.addLevelName(level=__trace_id, levelName="TRACE")

# defining logger
logger = Logger(name="automl_logger")
logger.addHandler(hdlr=hdlr)
logging.Logger.trace = trace
