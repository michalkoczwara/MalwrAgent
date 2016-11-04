# -*- coding: utf-8 -*-
"""the web module provides methods for HTTP communication"""
from __future__ import absolute_import

import requests
import validators

from urlparse import urlparse
from urlparse import parse_qsl  # return data as a list of name, value pairs
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
    def __parse_url(url):
        """return urlparsed url"""
        return urlparse(url, allow_fragments=False)

    @staticmethod
    def __get_parameter_from_parsed_url(parsed_url):
        """return target argument"""
        params = dict(parse_qsl(parsed_url.query, keep_blank_values=True))
        return params.keys()[0] if 0 < len(params.keys()) else None  # return the first argument only

    @staticmethod
    def __get_host_from_parsed_url(parsed_url):
        """return http(s) hostname"""
        return parsed_url.scheme + '://' + parsed_url.netloc

    @staticmethod
    def __validate_request_status(request):
        """validate a http request's response"""
        if request.status_code == 200:
            if request.text:
                return request.text
            else:
                return True  # req.text
        else:
            return False  # think about returning the req.status_code

    def __do_http_request(self, type_, url, data):
        """make http get and post requests"""
        parsed_url = self.__parse_url(url)
        parameter = self.__get_parameter_from_parsed_url(parsed_url)
        hostname = self.__get_host_from_parsed_url(parsed_url)
        url = hostname + parsed_url.path  # url is overwritten
        payload = {
            parameter: data
        }

        if type_ == 'GET':
            request = requests.get(url, payload)
        elif type_ == 'POST':
            request = requests.post(url, payload)

        return self.__validate_request_status(request)

    # how to ignore output ??
    @Decorators.args([('url', _FORMAT.URL)])
    @Decorators.config(run_first=True)
    def f_http_get(self, url):
        """send http get request"""
        input_ = self.settings['input']
        output = self.__do_http_request('GET', url, input_)
        return output

    @Decorators.args([('url', _FORMAT.URL)])
    @Decorators.config(run_first=True)
    def f_http_post(self, url):  # ask for two args, current only one supported
        """send http post request"""
        input_ = self.settings['input']
        output = self.__do_http_request('POST', url, input_)
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
