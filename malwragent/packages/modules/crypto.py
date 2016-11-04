# -*- coding: utf-8 -*-
"""the crypto module provides methods for encoding, hashing and encryption"""
from __future__ import absolute_import

import base64
import hashlib

from malwragent.packages.helpers.agentmodule import AgentModule
from malwragent.packages.helpers.agentmodule import Decorators

__class_name__ = 'Crypto'
# make mode hex???
__client_mode__ = True
__server_mode__ = True
__module_type__ = 'Transformation'


class Crypto(AgentModule):
    """provide basic crypto routines"""

    @staticmethod
    def __get_algorithms():
        """return available algorithms from hashlib"""
        return hashlib.algorithms_available

    # set(['SHA1', 'MDC2', 'SHA', 'SHA384', 'ecdsa-with-SHA1', 'SHA256',
    #     'SHA512', 'md4', 'md5', 'sha1', 'dsaWithSHA', 'DSA-SHA', 'sha',
    #     'sha224', 'dsaEncryption', 'DSA', 'ripemd160', 'mdc2', 'MD5',
    #     'MD4', 'sha384', 'SHA224', 'sha256', 'sha512', 'RIPEMD160'])

    def __calculate_hash(self, type_):
        """calculate hash based on type"""
        message_digest = None
        if type_ == 'md5':
            message_digest = hashlib.md5()
        elif type_ == 'sha1':
            message_digest = hashlib.sha1()
        elif type_ == 'sha256':
            message_digest = hashlib.sha256()

        message_digest.update(self.settings['input'])
        return message_digest.hexdigest()

    @Decorators.args(None)  # can be applied to methods, not a must
    def f_md5(self):
        """calculate md5 hash"""
        return self.__calculate_hash('md5')

    def f_sha1(self):
        """calculate sha1 hash"""
        return self.__calculate_hash('sha1')

    def f_sha256(self):
        """calculate sha256 hash"""
        return self.__calculate_hash('sha256')

    def f_base64_encode(self):
        """encode input with base64"""
        return base64.b64encode(self.settings['input'])

    def f_base64_decode(self):
        """decode input with base64"""
        return base64.b64decode(self.settings['input'])
