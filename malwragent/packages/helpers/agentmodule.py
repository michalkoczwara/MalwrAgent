# -*- coding: utf-8 -*-
from __future__ import absolute_import

from malwragent.packages.constants import ATTR_ARGS
from malwragent.packages.constants import ATTR_CONFIG

__class_name__ = 'AgentModule'


class AgentModule(object):
    """module class all modules inherit from"""

    def __init__(self, mode, settings):
        self.mode = mode
        self.output = None

        self.settings = settings.get('settings')
        self.function = self.settings.get('function')
        self.input = self.settings.get('input')
        self.args = self.settings.get('args')

        # print self.args

    def run(self):
        if hasattr(self, self.function):
            if self.args is None:
                self.output = getattr(self, self.function)()
            else:
                args = [y for x, y in self.args.iteritems()]
                # TODO check if callable
                # print args
                self.output = getattr(self, self.function)(*args)
        return self.output


##
# DECORATORS
##
class Decorators(object):

    @staticmethod
    def args(args):
        def wrapper(func):
            # print func.__name__
            # print args
            ATTR_ARGS[func.__name__] = args
            # print _ATTR_ARGS
            return func

        return wrapper

    @staticmethod
    def config(**kwargs):
        def wrapper(func):
            # print func.__name__
            # print kwargs
            # TODO remove test when ready
            for c in ['run_first', 'test']:
                if not ATTR_CONFIG.get(func.__name__, None):
                    ATTR_CONFIG[func.__name__] = dict()
                if c in kwargs:
                    ATTR_CONFIG[func.__name__].update({c: kwargs[c]})
                    # print _ATTR_CONFIG
            return func

        return wrapper
