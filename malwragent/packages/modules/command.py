from __future__ import absolute_import

import shlex
import subprocess

from malwragent.packages.malwragentmodules import MalwrAgentModule
from malwragent.packages.malwragentmodules import Decorators

__class_name__ = 'Command'
__client_mode__ = True
__server_mode__ = False
__module_type__ = 'Post'


class Command(MalwrAgentModule):
    """provides command execution routines"""

    @Decorators.args(None)
    def f_exec_system(self):
        input_ = self.settings['input']
        cli_and_args = shlex.split(input_)
        process = subprocess.Popen(cli_and_args, stdout=subprocess.PIPE)
        output = process.stdout.read().strip()
        return output
