from __future__ import absolute_import

import json
import logging
import pkgutil
import sys

from malwragent.packages import modules
from tabulate import tabulate
from termcolor import colored

from malwragent.packages.constants import ATTR_ARGS
from malwragent.packages.constants import ATTR_CONFIG
from malwragent.packages.helpers.rocketapi import RocketAPI

__class_name__ = 'ClientAPI'


class ClientAPI(object):
    def __init__(self, name='client', mode='client', logging_level=0, debug_level=0):
        # TODO save general settings in chain or
        #   at least in the json config dump
        self.master_chain = dict()

        # TODO run multiple chains simultaneously
        self.logging_level = logging_level
        self.debug_level = debug_level
        self.name = name
        self.mode = mode
        self.interval = 5
        self.interval_random = False

        # TODO create custom log/debug levels / centralized
        if self.logging_level == 1:
            logging.basicConfig(level=logging.ERROR)
        if self.logging_level == 2:
            logging.basicConfig(level=logging.WARN)
        if self.logging_level == 3:
            logging.basicConfig(level=logging.INFO)

    @staticmethod
    def exit(return_code):
        sys.exit(return_code)

    @staticmethod
    def get_import(module):
        # TODO[25/10/2016][bl4ckw0rm] malwragent.packages.modules - retrieve with function?
        return __import__('malwragent.packages.modules.' + module.lower(),
                          fromlist=[module])

    def set_client_name(self, name):
        self.name = name

    def set_client_interval(self, interval):
        self.interval = interval

    def log_info(self, msg):
        logging.info(self.name + ': ' + str(msg))

    def log_error(self, msg):
        logging.error(self.name + ': ' + str(msg))

    def log_fail(self, message, color='red'):
        print colored(self.name + ': ' + str(message), color)

    def log_success(self, message, color='green'):
        print colored(self.name + ': ' + str(message), color)

    def log_notice(self, message):
        print self.name + ': ' + message

    # TODO low: validate chain order for second,third ... module ???
    def validate_config(self, args=None, cur_idx=0):
        def do_validate(args=None):
            result = {'result': False, 'reason': '???', 'code': 500}

            if args is None:
                result = {'result': False, 'reason': 'Please do not act like a fool, try again', 'code': 501}
            else:
                settings = args.get('settings', None)
                function = settings.get('function', None)
                _args = settings.get('args', None)
                # print _args
                if function in ATTR_ARGS:
                    self.log_info('Checking ' + function + ' with parameters ' + str(_args))

                    required_args = None
                    required_format = None
                    if ATTR_ARGS[function]:
                        # Does only work with a single argument !!!
                        # print _ATTR_ARGS[function][0]
                        if isinstance(ATTR_ARGS[function][0], tuple):
                            required_args, required_format = ATTR_ARGS[function][0]
                            # print required_args
                            # print required_format
                        else:
                            required_args = ','.join(ATTR_ARGS[function])

                    if required_args is None and _args is None:
                        result = {'result': True}

                    # ARGS not provided
                    if required_args and _args is None:
                        result['reason'] = 'Please provide the following arguments: ' \
                                           + required_args
                        result['missing_args'] = required_args
                        result['code'] = 400

                    # ARGS provided but maybe incorrectly spelled
                    if required_args and _args:

                        # TODO do only ask for arguments not provided

                        result['reason'] = 'Please check the following arguments: ' \
                                           + required_args
                        result['code'] = 401

                        for _r in required_args.split(','):
                            # print _r,_args
                            if _r in _args:
                                # print "in",_args[_r]

                                # EMPTY
                                if not _args[_r]:
                                    result['reason'] = 'Empty value is not accepted'
                                    result['missing_args'] = _r
                                    result['code'] = 403
                                else:
                                    # NOT EMPTY
                                    if required_format:
                                        if not required_format.im_func(_args[_r]):
                                            result['reason'] = 'Format not valid'
                                            result['missing_args'] = _r
                                            result['code'] = 402
                                            # print _r,_args
                                        else:
                                            result = {'result': True}
                            else:
                                # ARRAY OR ,
                                # multiple arguments supported?
                                check_args = _r
                                result['missing_args'] = check_args
                                result['code'] = 404

            return result

        def do_validate_order(args, cur_idx):
            result = dict()
            result['result'] = False
            result['reason'] = 'Module cannot be run first in chain'
            result['code'] = 405

            # TODO def get args and return array with all information
            settings = args.get('settings', None)
            function = settings.get('function', None)
            config = ATTR_CONFIG.get(function, None)
            # print config

            if cur_idx < 1:
                # print config
                if config:
                    allowed_to_run_first_in_chain = config.get('run_first', None)
                    if allowed_to_run_first_in_chain:
                        result['result'] = True
            elif cur_idx >= 1:
                result['result'] = True

            return result

        result = do_validate_order(args, cur_idx)
        if not result['result']:
            return result

        result = do_validate(args)
        return result

    # TODO merge add module functions
    # TODO make a class for logging and debugging
    def add_module(self, chain, module, args=None, mode='auto'):
        def convert_to_text(module_name, args):
            text = ''
            text += 'Adding function '
            text += str(args['settings']['function'])
            text += ' from module '
            text += module_name
            text += ' with args <'
            text += str(args['settings']['args'])
            text += '>'  # done , failed
            return text

        module = self.get_import(module)
        # TODO def get and return module attrs
        module_name = module.__class_name__

        cur_chain_idx = self.get_chain_length()
        if cur_chain_idx:
            # TODO ERROR if CHAIN Key not in Dict()
            cur_chain_idx = self.get_chain_length_by_name(chain)

        result = self.validate_config(args, cur_idx=cur_chain_idx)

        self.log_info(result)

        if result['result'] is True:
            if self.debug_level > 1:
                self.log_success(convert_to_text(module_name, args) + ' done')

            if not self.master_chain.get(chain, None):
                self.master_chain[chain] = []

            # print self.master_chain

            self.master_chain[chain].append((module, args))
            if mode == 'interactive':
                return result
        elif result['result'] is False:
            if self.debug_level > 0:
                self.log_fail(result['reason'])
            if self.debug_level > 1:
                self.log_fail(convert_to_text(module_name, args) + ' failed')

            if mode == 'interactive':
                return result
            else:
                self.exit(2)

    # TODO
    # merge chains
    # find better way to concat chains for output format table

    def get_chain_by_name(self, chain_name, out_format='raw'):
        if out_format == 'raw':
            return self.master_chain[chain_name]
        elif out_format == 'table':
            # return table formatted
            result = []
            for item in self.master_chain[chain_name]:
                module, module_args = item
                mod_info = {
                    'chain': chain_name,
                    'module': module.__class_name__,
                    'type': module.__module_type__,
                    'function': module_args['settings']['function'],
                    'arguments': module_args['settings']['args']
                }

                result.append(mod_info)
            if result:
                result = tabulate(result, headers='keys', tablefmt='')
            else:
                result = 'EMPTY'
            return result

    # TODO
    # def get module attributes
    # array with mod info etc.
    def get_master_chain(self, out_format='raw'):
        if out_format == 'raw':
            return self.master_chain
        elif out_format == 'table':
            # TODO fancy flow chart ????
            result = []

            for chain_name, module in self.master_chain.iteritems():
                for item in module:
                    module, module_args = item
                    mod_info = {
                        'chain': chain_name,
                        'module': module.__class_name__,
                        'type': module.__module_type__,
                        'function': module_args['settings']['function'],
                        'arguments': module_args['settings']['args']
                    }

                    result.append(mod_info)

            # TODO combine with get_chain_by_name ??

            if result:
                result = tabulate(result, headers='keys', tablefmt='')
            else:
                result = 'EMPTY'
            return result

    def get_chain_length_by_name(self, chain):
        return len(self.get_chain_by_name(chain))

    def get_chain_length(self):
        return len(self.master_chain)

    @staticmethod
    def get_functions(class_):
        """get names from module namespace"""
        functions = []
        for name in dir(class_):
            if name.startswith('f_'):
                functions.append(name)
        return functions

    # TODO merge get_module and get_import
    def get_module(self, name):
        mod_info = {}
        for module_loader, module_name, is_pkg in pkgutil.iter_modules(modules.__path__):
            if module_name == name:
                module = module_loader.find_module(module_name).load_module(module_name)
                if hasattr(module, '__class_name__'):
                    if hasattr(module, '__client_mode__'):
                        if module.__client_mode__:
                            class_name = module.__class_name__
                            class_ = getattr(module, class_name)
                            functions = self.get_functions(class_)
                            mod_info['name'] = module_name
                            mod_info['class'] = class_name
                            mod_info['type'] = module.__module_type__
                            mod_info['functions'] = functions

                            return mod_info
        return False

    def get_module_list(self, out_format='raw'):
        module_list = []
        for module_loader, name, is_pkg in pkgutil.iter_modules(modules.__path__):
            module = self.get_module(name)
            if (module):
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

    def add_chain_to_master(self, chain):
        if not self.master_chain.get(chain, None):
            self.master_chain[chain] = []

    def load_chain_from_file(self, filename='config.json'):
        with open(filename) as infile:
            for item in json.load(infile):
                chain = item['chain']
                module = item['module']
                settings = item['settings']

                self.add_chain_to_master(chain)
                self.add_module(chain, module, {'settings': settings})

        if self.debug_level > 2:
            print self.master_chain

    def save_chain_to_file(self, filename='config.json'):
        chains = []

        for chain_name, module in self.master_chain.iteritems():
            for item in module:
                module, module_args = item
                mod_info = {
                    'chain': chain_name,
                    'module': module.__class_name__,
                    'type': module.__module_type__,
                    'settings': module_args['settings']
                }

                chains.append(mod_info)

        with open(filename, 'w') as outfile:
            json.dump(chains, outfile, indent=4)

    def rocket_api(self):
        rocket_api = RocketAPI(self.master_chain, self.name, self.mode,
                               interval=self.interval,
                               logging_level=self.logging_level,
                               debug_level=self.debug_level)
        rocket_api.main()
