# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pkgutil
import multiprocessing

from malwragent.packages import modules
from malwragent.packages.helpers.agent import Agent
from malwragent.packages.helpers.chain import Chain

__class_name__ = 'Client'


class Client(Chain):
    def __init__(self, name='client', mode='client', logging_level=0):
        super(Client, self).__init__(name, logging_level)

        # TODO save general settings in chain or at least in the json config dump

        self.name = name
        self.mode = mode
        self.interval = 5
        self.interval_random = False

        self.jobs = []

    def set_client_name(self, name):
        self.name = name

    def set_client_interval(self, interval):
        self.interval = interval

    @staticmethod
    def __get_functions(class_):
        """get names from module namespace"""
        functions = []
        for name in dir(class_):
            if name.startswith('f_'):
                functions.append(name)
        return functions

    # TODO merge get_module and get_import
    def __get_module(self, name):
        mod_info = {}
        for module_loader, module_name, is_pkg in pkgutil.iter_modules(modules.__path__):
            if module_name == name:
                module = module_loader.find_module(module_name).load_module(module_name)
                if hasattr(module, '__class_name__'):
                    if hasattr(module, '__client_mode__'):
                        if module.__client_mode__:
                            class_name = module.__class_name__
                            class_ = getattr(module, class_name)
                            functions = self.__get_functions(class_)
                            mod_info['name'] = module_name
                            mod_info['class'] = class_name
                            mod_info['type'] = module.__module_type__
                            mod_info['functions'] = functions

                            return mod_info
        return False

    def get_module_list(self, out_format='raw'):
        module_list = []
        for module_loader, name, is_pkg in pkgutil.iter_modules(modules.__path__):
            module = self.__get_module(name)
            if module:
                for function_name in module['functions']:
                    mod_info = {
                        'module': module['class'],
                        'type': module['type'],
                        'function': function_name
                    }
                    module_list.append(mod_info)

        if out_format == 'raw':
            return module_list
        elif out_format == 'select':
            count = 0
            for item in module_list:
                item['choice'] = count
                count += 1
            return module_list

    def run_agent(self):
        process = multiprocessing.Process(target=Agent,
                                          args=(self.name, self.mode, self.chain,
                                                self.interval, self.logging_level
                                                ))
        self.jobs.append(process)

        for j in self.jobs:
            j.start()

        for j in self.jobs:
            j.join()

