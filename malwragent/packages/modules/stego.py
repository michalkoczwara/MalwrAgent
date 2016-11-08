# -*- coding: utf-8 -*-
"""the stego module provides methods for hiding messages in text, images and videos"""
from __future__ import absolute_import

from stegano import lsb

from malwragent.packages.helpers.agentmodule import AgentModule

__class_name__ = 'Stego'
__client_mode__ = True
__server_mode__ = False
__module_type__ = 'Transformation'


class Stego(AgentModule):
    """provide basic stego routines"""

    def f_extract_text_from_image(self):
        """extract hidden text from an image object

        :rtype: String
        :return: A text, command string
        """
        try:
            output = lsb.reveal(self.input)
        except IOError:
            return False
        return str(output)
