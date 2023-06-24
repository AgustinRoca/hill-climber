"""DO NOT MODIFY THIS FILE"""

import logging

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    green = "\x1b[32;20m"
    bold_red = "\x1b[31;1m"
    reset = "" # "\x1b[0m"
    format = 'MountainServer [%(process)d] %(levelname)s: %(asctime)s - %(message)s'

    FORMATS = {
        logging.DEBUG: format + reset,
        logging.INFO: format + reset,
        logging.WARNING: format + reset,
        logging.ERROR: format + reset,
        logging.CRITICAL: format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
