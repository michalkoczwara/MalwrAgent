# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
from termcolor import colored


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

    def print_fail(self, msg, color='red'):
        print colored(self.name + ': ' + str(msg), color)

    def print_success(self, msg, color='green'):
        print colored(self.name + ': ' + str(msg), color)

    def print_notice(self, msg):
        print self.name + ': ' + str(msg)
