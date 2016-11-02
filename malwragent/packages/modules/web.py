# -*- coding: utf-8 -*-
"""the web module provides methods for HTTP communication"""
from __future__ import absolute_import

import requests
import validators

from cStringIO import StringIO

from malwragent.packages.helpers.agentmodule import AgentModule
from malwragent.packages.helpers.agentmodule import Decorators

__class_name__ = 'Web'
__client_mode__ = True
__server_mode__ = True
__module_type__ = 'Transportation'


class _FORMAT(object):
    URL = validators.url


class Web(AgentModule):
    """provide basic transportation routines"""

    @staticmethod
    def __do_get(url, data):
        """process url,data and make HTTP GET request"""
        # TODO[25/10/2016][bl4ckw0rm] do this better
        # TODO[30/10/2016][bl4ckw0rm] validate URI for its domain, path and parameter
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
            return False  # think about returning the req.status_code

    @staticmethod
    def __do_post(url, data):
        """process url,data and make HTTP POST request"""
        payload = {
            'param': data
        }

        req = requests.post(url, payload)
        # print req.status_code
        if req.status_code == 200:
            if req.text:
                return req.text
            else:
                return True  # req.text
        else:
            return False  # think about returning the req.status_code

    @Decorators.args([('url', _FORMAT.URL)])
    @Decorators.config(run_first=True)
    def f_http_get(self, url):
        """send HTTP GET request"""
        input_ = self.settings['input']
        output = self.__do_get(url, input_)
        return output

    @Decorators.args([('url', _FORMAT.URL), 'parameter'])
    @Decorators.config(run_first=True)
    def f_http_post(self, url):  # ask for two args, current only one supported
        """send HTTP POST request"""
        input_ = self.settings['input']
        output = self.__do_post(url, input_)
        return output

    @staticmethod
    @Decorators.args([('url', _FORMAT.URL)])
    @Decorators.config(run_first=True)
    def f_retrieve_image(url):
        """retrieve an image, image is stored in memory only
        :rtype: StringIO object
        :param url: Image URL
        :return: Object of image
        """
        output = StringIO(requests.get(url).content)  # Use BytesIO
        return output
