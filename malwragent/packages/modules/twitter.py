# -*- coding: utf-8 -*-
from __future__ import absolute_import

import requests
import re

from BeautifulSoup import BeautifulSoup as soupy
from malwragent.packages.helpers.agentmodule import AgentModule
from malwragent.packages.helpers.agentmodule import Decorators

__class_name__ = 'Twitter'
__client_mode__ = True
__server_mode__ = False
__module_type__ = 'Transportation'


class Twitter(AgentModule):
    """provides basic twitter communication routines"""

    @staticmethod
    @Decorators.args(['profile_name'])
    @Decorators.config(run_first=True)
    def f_grab_cmd_from_twitter_profile(profile_name):
        """Grab 0xXXXXXXXX tag from Profile, Tag must match [a-zA-Z0-9_]
        :rtype: string
        :param profile_name: twitter profile name without leading @
        :return: string embedded in the profile description
        """
        url = 'https://twitter.com/%(profile)s'
        payload = {
            'profile': profile_name
        }
        html = requests.get(url % payload)
        soup = soupy(html.text)
        profile_description = soup.find('meta', {'name': 'description'})['content']
        match = re.search('(0x)\w+', profile_description)
        output = match.group(0)

        return str(output)
