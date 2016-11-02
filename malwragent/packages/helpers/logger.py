# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

__class_name__ = 'Logger'


class Logger(object):
    def __init__(self, name, logging_level):
        self.name = name
        self.logging_level = logging_level

        if self.logging_level == 1:
            logging.basicConfig(level=logging.ERROR)
        if self.logging_level == 2:
            logging.basicConfig(level=logging.WARN)
        if self.logging_level == 3:
            logging.basicConfig(level=logging.INFO)
        if self.logging_level == 4:
            logging.basicConfig(level=logging.DEBUG)

        # Suppress logging for the PIL.Image module but CRITICAL
        logging.getLogger("PIL").setLevel(logging.CRITICAL)

    def log_debug(self, msg):
        logging.debug(self.name + ': ' + str(msg))

    def log_info(self, msg):
        logging.info(self.name + ': ' + str(msg))

    def log_warning(self, msg):
        logging.warning(self.name + ': ' + str(msg))

    def log_error(self, msg):
        logging.error(self.name + ': ' + str(msg))

    def log_critical(self, msg):
        logging.critical(self.name + ': ' + str(msg))
