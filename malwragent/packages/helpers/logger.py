# -*- coding: utf-8 -*-
"""the logger helper provides centralized logging"""
from __future__ import absolute_import

import logging

__class_name__ = 'Logger'


class Logger(object):
    """provide basic logging methods"""
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

    def __build_log_string(self, msg):
        """concat the log string"""
        return "%s:%s" % (self.name, msg)

    def __do_log(self, type_, msg):
        """do the actual logging"""
        message = self.__build_log_string(msg)
        if type_ == 'DEBUG':
            logging.debug(message)
        elif type_ == 'INFO':
            logging.info(message)
        elif type_ == 'WARNING':
            logging.warning(message)
        elif type_ == 'ERROR':
            logging.error(message)
        elif type_ == 'CRITICAL':
            logging.critical(message)

    def log_debug(self, msg):
        """log a debug message"""
        self.__do_log('DEBUG', msg)

    def log_info(self, msg):
        """log a informational message"""
        self.__do_log('INFO', msg)

    def log_warning(self, msg):
        """log a warning message"""
        self.__do_log('WARNING', msg)

    def log_error(self, msg):
        """log an error message"""
        self.__do_log('ERROR', msg)

    def log_critical(self, msg):
        """log a critical message"""
        self.__do_log('CRITICAL', msg)
