# -*- coding: utf-8 -*-

import logging
import os
import sys
import time

from termcolor import colored


class MalwrRocket(object):
    def __init__(self, name, mode, chain, interval, logging_level=0, debug_level=0):
        self.name = name
        self.mode = mode
        self.chain = chain
        self.interval = interval
        self.pid = str(os.getpid())
        if hasattr(os, 'getppid'):  # only available on Unix
            self.ppid = str(os.getppid())
        # self.job_id = job_id
        self.registered = False
        self.logging_level = logging_level
        self.debug_level = debug_level

        # print self.logging_level
        # print self.debug_level
        try:
            if self.debug_level > 0:
                self.log_success('Starting new process with PID ' + self.pid)
            self.run()
        except KeyboardInterrupt:
            pass

    @staticmethod
    def exit(return_code):
        sys.exit(return_code)

    def log_info(self, msg):
        logging.info(self.name + ':' + self.pid + ' ' + str(msg))

    def log_error(self, msg):
        logging.error(self.name + ':' + self.pid + ' ' + str(msg))

    def log_fail(self, message, color='red'):
        print colored(self.name + ':' + self.pid + ' ' + str(message), color)

    def log_success(self, message, color='green'):
        print colored(self.name + ':' + self.pid + ' ' + str(message), color)

    def log_notice(self, message):
        print self.name + ':' + self.pid + ' ' + message

    def run(self):
        # START inner functions
        def run_registration():
            #print self.chain

            if self.debug_level > 0:
                self.log_success('Chain ' + 'REG' + ' running')
            result = run_single_chain(self.chain['REG'])

            if self.debug_level > 0:
                self.log_success('Chain ' + 'REG' + ' finished')

            if result:
                self.registered = True
                msg = 'Client registration successful'
                if self.debug_level > 0:
                    self.log_success(msg)
                self.log_info(msg)

                del self.chain['REG']

            else:
                msg = 'Client registration failed'
                if self.debug_level > 0:
                    self.log_fail(msg)
                self.log_error(msg)
                # self.exit(2)

            # TODO retry when failed

        def convert_to_text(module_name, args):
            # print args
            text = ''
            text += 'Running function '
            text += str(args['settings']['function'])
            text += ' from module '
            text += module_name
            text += ' with input <'
            text += str(args['settings']['input'])
            text += '> and args <'
            text += str(args['settings']['args'])
            text += '>'
            return text

        def run_module(module, args=None):
            module_type = str(module.__module_type__)
            module_name = str(module.__class_name__)
            # self.log_info(args)

            if self.debug_level > 1:
                self.log_notice(convert_to_text(module_name, args))

            self.log_info("Running " + module_type + " module " + \
                          str(module.__name__) + "." + module_name + \
                          " - Args: " + str(args))

            instance = getattr(module, module.__class_name__)(self.mode, args)
            result = False
            # has instance a def run
            if hasattr(instance, 'run'):
                # call def run in instance
                result = getattr(instance, 'run')()
            return result

        def validate_result(result):
            def handle_error_code():
                pass

            # ERROR "CODE" HANDLING

            # TODO
            #
            # output: use it to stop the thread?
            # for self shutdown?
            # secret code to shutdown/self destruct the malwr?
            #

            # do special processing in here
            # perhaps shutdown initiated from a module

            # self.log_info(result)

            # TODO: error handling
            if self.debug_level > 2:
                self.log_notice('Result validation ' + str(type(result)) + ' ' + str(result))

            # TODO This is only very trivial
            if not result and not None:
                return False
            else:
                return True

        def run_single_chain(chain):
            retry_cnt = 3
            input_ = None
            timeout = 5
            run_next = None

            for item in chain:
                module, args = item
                args['settings']['input'] = input_

                try_cnt = 1
                while try_cnt <= retry_cnt:
                    output = run_module(module, args=args)
                    run_next = validate_result(output)
                    if run_next:
                        # output from module becomes input for next module
                        input_ = output
                        break
                    else:
                        time.sleep(timeout)

                    if try_cnt == retry_cnt:
                        return False
                    else:
                        try_cnt += 1

            return run_next

        def run_client():
            while True:
                # TODO how to run multiple chains async ??? this an malwragent issue

                if self.debug_level > 0:
                    self.log_success('Chain ' + 'CLIENT' + ' running')

                result = run_single_chain(self.chain['CLIENT'])

                if self.debug_level > 0:
                    if result:
                        self.log_success('Chain ' + 'CLIENT' + ' finished')
                    else:
                        self.log_error('Chain ' + 'CLIENT' + ' finished with errors')

                # TODO random sleep
                if self.debug_level > 2:
                    self.log_notice('Sleeping ' + str(self.interval) + ' seconds')

                time.sleep(self.interval)

        # END inner functions

        if self.chain.get('REG', None):
            run_registration()

            if self.registered:
                run_client()
        else:
            # run without registration
            # e.g. do only egress testing
            run_client()
