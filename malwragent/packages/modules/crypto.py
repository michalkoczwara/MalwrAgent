# -*- coding: utf-8 -*-
from __future__ import absolute_import

import base64
import hashlib

from malwragent.packages.malwragentmodules import MalwrAgentModule
from malwragent.packages.malwragentmodules import Decorators

__class_name__ = 'Crypto'
# make mode hex???
__client_mode__ = True
__server_mode__ = True
__module_type__ = 'Transformation'


class Crypto(MalwrAgentModule):
    """provides crypto routines"""

    @staticmethod
    def __get_algorithms():
        # print dir(hashlib)
        return hashlib.algorithms_available

        # set(['SHA1', 'MDC2', 'SHA', 'SHA384', 'ecdsa-with-SHA1', 'SHA256',

    #     'SHA512', 'md4', 'md5', 'sha1', 'dsaWithSHA', 'DSA-SHA', 'sha',
    #     'sha224', 'dsaEncryption', 'DSA', 'ripemd160', 'mdc2', 'MD5',
    #     'MD4', 'sha384', 'SHA224', 'sha256', 'sha512', 'RIPEMD160'])

    @Decorators.args(None)
    def f_md5(self):
        input_ = self.settings['input']
        # print self.mode
        m = hashlib.md5()
        m.update(input_)
        return m.hexdigest()

    @Decorators.args(None)
    def f_sha1(self):
        input_ = self.settings['input']
        # print self.mode
        m = hashlib.sha1()
        m.update(input_)
        return m.hexdigest()

    @Decorators.args(None)
    def f_sha256(self):
        input_ = self.settings['input']
        # print self.mode
        m = hashlib.sha256()
        m.update(input_)
        return m.hexdigest()

    @Decorators.args(None)
    def f_base64_encode(self):
        input_ = self.settings['input']
        return base64.b64encode(input_)

    @Decorators.args(None)
    def f_base64_decode(self):
        input_ = self.settings['input']
        return base64.b64decode(input_)
