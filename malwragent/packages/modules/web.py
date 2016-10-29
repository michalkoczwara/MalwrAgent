# -*- coding: utf-8 -*-
from __future__ import absolute_import

import requests
import validators

from malwragent.packages.helpers.agentmodule import AgentModule
from malwragent.packages.helpers.agentmodule import Decorators

__class_name__ = 'Web'
__client_mode__ = True
__server_mode__ = True
__module_type__ = 'Transportation'


class _FORMAT(object):
    URL = validators.url


class Web(AgentModule):
    """provides basic transportation routines"""
    # TODO[25/10/2016][bl4ckw0rm] Provide request timeout and ERROR handling
    """
    Process Process-1:
    Traceback (most recent call last):
      File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/multiprocessing/process.py", line 258, in _bootstrap
        self.run()
      File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/multiprocessing/process.py", line 114, in run
        self._target(*self._args, **self._kwargs)
      File "/Users/bl4ckw0rm/PycharmProjects/MalwrAgent/malwragent/packages/agent.py", line 30, in __init__
        self.run()
      File "/Users/bl4ckw0rm/PycharmProjects/MalwrAgent/malwragent/packages/agent.py", line 193, in run
        run_client()
      File "/Users/bl4ckw0rm/PycharmProjects/MalwrAgent/malwragent/packages/agent.py", line 178, in run_client
        result = run_single_chain(self.chain['CLIENT'])
      File "/Users/bl4ckw0rm/PycharmProjects/MalwrAgent/malwragent/packages/agent.py", line 156, in run_single_chain
        output = run_module(module, args=args)
      File "/Users/bl4ckw0rm/PycharmProjects/MalwrAgent/malwragent/packages/agent.py", line 113, in run_module
        result = getattr(instance, 'run')()
      File "/Users/bl4ckw0rm/PycharmProjects/MalwrAgent/malwragent/packages/agentmodule.py", line 29, in run
        self.output = getattr(self, self.function)(*args)
      File "/Users/bl4ckw0rm/PycharmProjects/MalwrAgent/malwragent/packages/modules/web.py", line 47, in f_http_get
        input_ = self.settings['input']
      File "/Users/bl4ckw0rm/PycharmProjects/MalwrAgent/malwragent/packages/modules/web.py", line 29, in __do_get

      File "/Library/Python/2.7/site-packages/requests/api.py", line 70, in get
        return request('get', url, params=params, **kwargs)
      File "/Library/Python/2.7/site-packages/requests/api.py", line 56, in request
        return session.request(method=method, url=url, **kwargs)
      File "/Library/Python/2.7/site-packages/requests/sessions.py", line 475, in request
        resp = self.send(prep, **send_kwargs)
      File "/Library/Python/2.7/site-packages/requests/sessions.py", line 596, in send
        r = adapter.send(request, **kwargs)
      File "/Library/Python/2.7/site-packages/requests/adapters.py", line 473, in send
        raise ConnectionError(err, request=request)
    ConnectionError: ('Connection aborted.', BadStatusLine("''",))
    """
    @staticmethod
    def __do_get(url, data):
        # TODO[25/10/2016][bl4ckw0rm] do this better
        if data is not None:
            uri = '%s%s' % (url, data)
        else:
            uri = '%s' % url

        req = requests.get(uri)
        # print req.status_code
        if req.status_code == 200:
            if req.text:
                return req.text
            else:
                return True  # req.text
        else:
            return False  # req.status_code

    @staticmethod
    def __do_post(url, data):
        return False  # req.status_code

    @Decorators.args([('url', _FORMAT.URL)])
    @Decorators.config(run_first=True)
    def f_http_get(self, url):
        """HTTP GET Request"""
        input_ = self.settings['input']
        output = self.__do_get(url, input_)
        return output

    @Decorators.args([('url', _FORMAT.URL)])
    @Decorators.config(run_first=True)
    def f_http_post(self, url):
        """HTTP POST Request"""
        input_ = self.settings['input']
        output = self.__do_post(url, input_)
        return output
