#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from malwragent.packages.helpers.client import Client

__CHAIN_ID = 'CLIENT'
__CLIENT = Client(logging_level=4)
__CLIENT.set_client_name('pytest')


# test run first
def test_crypto_f_md5():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_md5',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Crypto', module_args, mode='interactive')
    assert result['result'] is False and result['code'] == 405


def test_enumeration_f_get_platform():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_get_platform',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Enumeration', module_args, mode='interactive')
    assert result['result'] is True


def test_enumeration_f_get_platform_version():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_get_platform_version',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Enumeration', module_args, mode='interactive')
    assert result['result'] is True


def test_enumeration_f_get_platform_machine():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_get_platform_machine',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Enumeration', module_args, mode='interactive')
    assert result['result'] is True


def test_enumeration_f_get_platform_system():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_get_platform_system',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Enumeration', module_args, mode='interactive')
    assert result['result'] is True


def test_enumeration_f_get_platform_processor():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_get_platform_processor',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Enumeration', module_args, mode='interactive')
    assert result['result'] is True


def test_enumeration_f_get_platform_uname():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_get_platform_uname',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Enumeration', module_args, mode='interactive')
    assert result['result'] is True


def test_crypto_f_sha1():
    # do not clear chain here
    module_args = {
        'settings': {
            'function': 'f_sha1',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Crypto', module_args, mode='interactive')
    assert result['result'] is True


def test_crypto_f_sha256():
    # do not clear chain here
    module_args = {
        'settings': {
            'function': 'f_sha256',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Crypto', module_args, mode='interactive')
    assert result['result'] is True


def test_crypto_f_base64_encode():
    # do not clear chain here
    module_args = {
        'settings': {
            'function': 'f_base64_encode',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Crypto', module_args, mode='interactive')
    assert result['result'] is True


def test_crypto_f_base64_decode():
    # do not clear chain here
    module_args = {
        'settings': {
            'function': 'f_base64_decode',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Crypto', module_args, mode='interactive')
    assert result['result'] is True


def test_twitter_f_grab_cmd_from_twitter_profile():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_grab_cmd_from_twitter_profile',
            'args': {
                'profile_name': 'test_profile_name'
            }
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Twitter', module_args, mode='interactive')
    assert result['result'] is True


def test_web_f_http_get_1():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_http_get',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Web', module_args, mode='interactive')
    assert result['result'] is False and result['code'] == 400  # Argument not provided


def test_web_f_http_get_2():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_http_get',
            'args': {
                'url': ''
            }
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Web', module_args, mode='interactive')
    assert result['result'] is False and result['code'] == 403  # Argument provided but empty


def test_web_f_http_get_3():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_http_get',
            'args': {
                'url': 'test_url_fail'
            }
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Web', module_args, mode='interactive')
    assert result['result'] is False and result['code'] == 402  # Argument provided but format invalid


def test_web_f_http_get_4():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_http_get',
            'args': {
                'url': 'http://mfs-enterprise.com'
            }
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Web', module_args, mode='interactive')
    assert result['result'] is True


def test_web_f_http_post():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_http_post',
            'args': {
                'url': 'http://mfs-enterprise.com'
            }
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Web', module_args, mode='interactive')
    assert result['result'] is True


def test_web_f_retrieve_image():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_retrieve_image',
            'args': {
                'url': 'http://mfs-enterprise.com'
            }
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Web', module_args, mode='interactive')
    assert result['result'] is True


def test_stego_f_extract_text_from_image_1():
    module_args = {
        'settings': {
            'function': 'f_extract_text_from_image',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Stego', module_args, mode='interactive')
    assert result['result'] is True


def test_f_exec_system():
    module_args = {
        'settings': {
            'function': 'f_exec_system',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Command', module_args, mode='interactive')
    assert result['result'] is True


def test_stego_f_extract_text_from_image_2():
    __CLIENT.clear_chain()
    module_args = {
        'settings': {
            'function': 'f_extract_text_from_image',
            'args': None
        }
    }
    result = __CLIENT.add_item(__CHAIN_ID, 'Stego', module_args, mode='interactive')
    assert result['result'] is False  # Cannot be run first


