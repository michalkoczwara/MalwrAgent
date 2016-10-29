# -*- coding: utf-8 -*-
from __future__ import absolute_import

import shlex
import subprocess

from malwragent.packages.helpers.agentmodule import AgentModule
from malwragent.packages.helpers.agentmodule import Decorators

__class_name__ = 'Command'
__client_mode__ = True
__server_mode__ = False
__module_type__ = 'Post'


class Command(AgentModule):
    """provides command execution routines"""

    @Decorators.args(None)
    def f_exec_system(self):
        input_ = self.settings['input']
        cli_and_args = shlex.split(input_)
        process = subprocess.Popen(cli_and_args, stdout=subprocess.PIPE)
        output = process.stdout.read().strip()
        return output
