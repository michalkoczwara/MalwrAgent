from __future__ import absolute_import

import platform

from malwragent.packages.malwragentmodules import MalwrAgentModule
from malwragent.packages.malwragentmodules import Decorators

__class_name__ = 'Enumeration'
__client_mode__ = True
__server_mode__ = False
__module_type__ = 'Post'


class Enumeration(MalwrAgentModule):
    """provides host enumeration routines"""

    @Decorators.args(None)
    @Decorators.config(run_first=True)
    def f_get_platform(self):
        return platform.platform()

    @Decorators.args(None)
    @Decorators.config(run_first=True)
    def f_get_platform_version(self):
        return platform.version()

    @Decorators.args(None)
    @Decorators.config(run_first=True)
    def f_get_platform_machine(self):
        return platform.machine()

    @Decorators.args(None)
    @Decorators.config(run_first=True)
    def f_get_platform_system(self):
        return platform.system()

    @Decorators.args(None)
    @Decorators.config(run_first=True)
    def f_get_platform_processor(self):
        return platform.processor()

    @Decorators.args(None)
    @Decorators.config(run_first=True)
    def f_get_platform_uname(self):
        return str(platform.uname())
