#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from malwragent.packages.helpers.client import Client

__CHAIN_ID = 'CLIENT'
__CLIENT = Client(logging_level=4)
__CLIENT.set_client_name('pytest')
__CLIENT.set_client_interval(0)  # only run once
__CLIENT.load_chain_from_file('./myChains/apt29.json')
__CLIENT.run_agent()


def test_apt29_client():
    assert __CLIENT.get_results() is True
