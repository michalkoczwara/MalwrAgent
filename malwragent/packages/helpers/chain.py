# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from tabulate import tabulate

from malwragent.packages.constants import ATTR_ARGS
from malwragent.packages.constants import ATTR_CONFIG

from malwragent.packages.helpers.logger import Logger

__class_name__ = 'Chain'


class Chain(object):
    def __init__(self, name, logging_level):
        # start with an empty chain
        self.chain = dict()
        self.name = name
        self.logging_level = logging_level

        self.logger = Logger(self.name, self.logging_level)

        # TODO[29/10/2016][bl4ckw0rm] implement chain uuid

    @staticmethod
    def __get_import(module):
        # TODO[25/10/2016][bl4ckw0rm] malwragent.packages.modules - retrieve with function?
        return __import__('malwragent.packages.modules.' + module.lower(),
                          fromlist=[module])

    def init_chain(self, chain_id):
        if not self.chain.get(chain_id, None):
            self.chain[chain_id] = []

    def get_chain_length(self):
        return len(self.chain)

    def get_chain_length_by_id(self, chain_id):
        return len(self.get_chain_by_id(chain_id))

    def get_chain_by_id(self, chain_id, out_format='raw'):
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
    def __validate_config(self, mod_idx, args=None):
        # START inner functions
        def __do_validate():
            _result = {'result': False, 'reason': '???', 'code': 500}

            if args is None:
                _result = {'result': False, 'reason': 'Please do not act like a fool, try again', 'code': 501}
            else:
                settings = args.get('settings', None)
                function = settings.get('function', None)
                _args = settings.get('args', None)
                # print _args
                if function in ATTR_ARGS:
                    self.logger.log_info('Checking ' + function + ' with parameters ' + str(_args))

                    required_args = None
                    required_format = None
                    if ATTR_ARGS[function]:
                        # Does only work with one argument !!!
                        # print _ATTR_ARGS[function][0]
                        if isinstance(ATTR_ARGS[function][0], tuple):
                            required_args, required_format = ATTR_ARGS[function][0]
                            # print required_args
                            # print required_format
                        else:
                            required_args = ','.join(ATTR_ARGS[function])

                    if required_args is None and _args is None:
                        _result = {'result': True}

                    # ARGS not provided
                    if required_args and _args is None:
                        _result['reason'] = 'Please provide the following arguments: ' \
                                           + required_args
                        _result['missing_args'] = required_args
                        _result['code'] = 400

                    # ARGS provided but maybe incorrectly spelled
                    if required_args and _args:
                        _result['reason'] = 'Please check the following arguments: ' \
                                           + required_args
                        _result['code'] = 401

                        for _r in required_args.split(','):
                            # print _r,_args
                            if _r in _args:
                                # print "in",_args[_r]

                                # EMPTY
                                if not _args[_r]:
                                    _result['reason'] = 'Empty value is not accepted'
                                    _result['missing_args'] = _r
                                    _result['code'] = 403
                                else:
                                    # NOT EMPTY
                                    if required_format:
                                        if not required_format.im_func(_args[_r]):
                                            _result['reason'] = 'Format not valid'
                                            _result['missing_args'] = _r
                                            _result['code'] = 402
                                            # print _r,_args
                                        else:
                                            _result = {'result': True}
                            else:
                                # TODO[30/10/2016][bl4ckw0rm] ARRAY OR multiple arguments supported ?
                                check_args = _r
                                _result['missing_args'] = check_args
                                _result['code'] = 404

            return _result

        def __do_validate_module_order():
            _result = dict()
            _result['result'] = False
            _result['reason'] = 'Module cannot be run first in chain'
            _result['code'] = 405

            settings = args.get('settings', None)
            function = settings.get('function', None)
            config = ATTR_CONFIG.get(function, None)

            if mod_idx < 1:
                if config:
                    allowed_to_run_first_in_chain = config.get('run_first', None)
                    if allowed_to_run_first_in_chain:
                        _result['result'] = True
            elif mod_idx >= 1:
                _result['result'] = True

            return _result

        # END inner functions

        result = __do_validate_module_order()
        if result['result']:
            result = __do_validate()

        return result

    def add_item(self, chain_id, module, args=None, mode='auto'):
        def convert_to_text(_module_name):
            text = ''
            text += 'Adding function '
            text += str(args['settings']['function'])
            text += ' from module '
            text += _module_name
            text += ' with args <'
            text += str(args['settings']['args'])
            text += '>'
            return text

        """ loading module first to run decorators """
        module = self.__get_import(module)
        module_name = module.__class_name__

        module_idx = self.get_chain_length_by_id(chain_id)
        result = self.__validate_config(module_idx, args)
        self.logger.log_debug(result)

        if result['result'] is True:
            self.logger.log_debug(convert_to_text(module_name) + ' done')

            self.chain[chain_id].append((module, args))
            if mode == 'interactive':
                return result
        elif result['result'] is False:
            self.logger.log_debug(convert_to_text(module_name) + ' failed')

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
