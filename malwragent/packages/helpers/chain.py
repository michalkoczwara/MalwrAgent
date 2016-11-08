# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from tabulate import tabulate

from malwragent.packages.constants import ATTR_ARGS
from malwragent.packages.constants import ATTR_CONFIG

from malwragent.packages.helpers.logger import Logger

__class_name__ = 'Chain'


class Chain(object):
    """the chain class consists of all methods needed to create a client's chain"""
    def __init__(self, name, logging_level):
        # start with an empty chain
        self.chain = {
            'CLIENT': []
        }
        self.name = name
        self.logging_level = logging_level

        self.logger = Logger(self.name, self.logging_level)

        # TODO[29/10/2016][bl4ckw0rm] implement chain uuid

    @staticmethod
    def __get_import(module):
        """import a module from the modules directory"""
        # TODO[25/10/2016][bl4ckw0rm] malwragent.packages.modules - retrieve with function?
        return __import__('malwragent.packages.modules.' + module.lower(),
                          fromlist=[module])

    def set_chain(self, chain):
        """set chain"""
        self.chain = chain

    def init_chain(self, chain_id):
        """initiate a chain by its ID"""
        if not self.chain.get(chain_id, None):
            self.chain[chain_id] = []

    def clear_chain(self):
        """set chain to its default"""
        self.chain = {
            'CLIENT': []
        }

    def clear_chain_by_id(self, chain_id):
        """set specific chain to its default, identified by ID"""
        self.chain[chain_id] = []

    def get_chain_length(self):
        """get a chain's length"""
        return len(self.chain)

    def get_chain_length_by_id(self, chain_id):
        """get a chain's length, identified by ID"""
        return len(self.get_chain_by_id(chain_id))

    def get_chain_by_id(self, chain_id, out_format='raw'):
        """get a chain, identified by ID"""
        if out_format == 'raw':
            return self.chain[chain_id]
        elif out_format == 'table':
            # return table formatted
            result = []
            for item in self.chain[chain_id]:
                module, module_args = item
                mod_info = {
                    'chain': chain_id,
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

    # TODO low: validate chain order for second,third ... module ???
    def __validate_config(self, module_idx, module_args):
        """validate a chain's configuration based on module order and argument format"""

        settings = module_args.get('settings', None)
        function = settings.get('function', None)
        config = ATTR_CONFIG.get(function, None)
        user_provided_arguments = settings.get('args', None)

        # START inner functions

        def __do_validate():
            _result = {'result': False, 'reason': '???', 'code': 500}

            if module_args is None:
                _result = {'result': False, 'reason': 'Please do not act like a fool, try again', 'code': 501}
            else:
                if function in ATTR_ARGS:
                    self.logger.log_debug('Checking ' + function + ' with parameters ' + str(user_provided_arguments))

                    # Normalize required arguments
                    required_args = []
                    if ATTR_ARGS[function]:
                        for argument in ATTR_ARGS[function]:
                            if isinstance(argument, tuple):
                                required_args.append(argument)
                            else:
                                required_args.append((argument, None))

                    if not required_args and user_provided_arguments is None:
                        _result = {'result': True}

                    # ARGS not provided
                    if required_args and user_provided_arguments is None:
                        _result['reason'] = 'Please provide the following arguments: ' \
                                            + ','.join([a for a, f in required_args])
                        _result['missing_args'] = [a for a, f in required_args]
                        _result['code'] = 400

                    # ARGS provided but maybe incorrectly spelled, or invalid formatted
                    if required_args and user_provided_arguments:
                        _result = {
                            'result': True
                        }

                        missing_arguments = []
                        for argument, required_format in required_args:
                            if argument in user_provided_arguments:
                                # EMPTY
                                if not user_provided_arguments[argument]:
                                    _result = {
                                        'result': False,
                                        'reason': 'Empty value is not accepted',
                                        'code': 403
                                    }

                                    missing_arguments.append(argument)
                                    break
                                else:
                                    # NOT EMPTY
                                    if required_format:
                                        if not required_format.im_func(user_provided_arguments[argument]):
                                            _result = {
                                                'result': False,
                                                'reason': 'Format not valid',
                                                'code': 402
                                            }

                                            missing_arguments.append(argument)
                                            break

                        if not _result['result']:
                            _result['missing_args'] = missing_arguments
                else:
                    # function is not in required argument list
                    _result = {
                        'result': True,
                        'code': 200
                    }

            return _result

        def __do_validate_module_order():
            _result = {
                'result': False,
                'reason': 'Module cannot be run first in chain',
                'code': 405
            }

            if module_idx < 1:
                if config:
                    if config.get('run_first', None):
                        _result['result'] = True
            elif module_idx >= 1:
                _result['result'] = True

            return _result

        # END inner functions

        result = __do_validate_module_order()
        if result['result']:
            result = __do_validate()

        return result

    def add_item(self, chain_id, module, module_args, mode='auto'):
        def convert_to_text(_module_name):
            text = ''
            text += 'Adding function '
            text += str(module_args['settings']['function'])
            text += ' from module '
            text += _module_name
            text += ' with args <'
            text += str(module_args['settings']['args'])
            text += '>'
            return text

        # loading module first to have decorators run
        module = self.__get_import(module)
        module_name = module.__class_name__

        module_idx = self.get_chain_length_by_id(chain_id)
        result = self.__validate_config(module_idx, module_args)
        self.logger.log_debug(result)

        if result['result'] is True:
            self.logger.log_info(convert_to_text(module_name) + ' done')
            self.chain[chain_id].append((module, module_args))
            if mode == 'interactive':
                return result
        elif result['result'] is False:
            self.logger.log_critical(convert_to_text(module_name) + ' failed')
            if mode == 'interactive':
                return result
            else:
                return False

    # TODO[30/10/2016][bl4ckw0rm] find better way to concat chains for output format table
    # TODO[30/10/2016][bl4ckw0rm] combine with get_chain_by_name ??
    def get_formatted_chain(self, out_format='json'):
        if out_format == 'json':
            # TODO[30/10/2016][bl4ckw0rm] Encode chain to json, module imports not serializeable
            return repr(self.chain)
        elif out_format == 'table':
            # TODO fancy flow chart ????
            result = []

            for chain_id, module in self.chain.iteritems():
                for item in module:
                    module, module_args = item
                    mod_info = {
                        'chain': chain_id,
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

    def load_chain_from_file(self, filename):
        with open(filename) as infile:
            for item in json.load(infile):
                chain_id = item['chain']
                module = item['module']
                settings = item['settings']

                self.init_chain(chain_id)
                self.add_item(chain_id, module, {'settings': settings})

        self.logger.log_debug(self.get_formatted_chain())

    def save_chain_to_file(self, filename):
        chain = []
        for chain_name, module in self.chain.iteritems():
            for item in module:
                module, module_args = item
                mod_info = {
                    'chain': chain_name,
                    'module': module.__class_name__,
                    'type': module.__module_type__,
                    'settings': module_args['settings']
                }

                chain.append(mod_info)

        with open(filename, 'w') as outfile:
            json.dump(chain, outfile, indent=4)
