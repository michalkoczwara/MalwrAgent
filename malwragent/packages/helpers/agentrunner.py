# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
import multiprocessing

from malwragent.packages.helpers.agent import Agent

__class_name__ = 'AgentRunner'


class AgentRunner(object):
    def __init__(self, master_chain, name, mode, interval, logging_level=0, debug_level=0):
        self.master_chain = master_chain
        self.name = name
        self.mode = mode
        self.interval = interval
        self.logging_level = logging_level
        self.debug_level = debug_level
        self.jobs = []

        # TODO make class for logging and debugging
        if self.logging_level == 1:
            logging.basicConfig(level=logging.ERROR)
        if self.logging_level == 2:
            logging.basicConfig(level=logging.WARN)
        if self.logging_level == 3:
            logging.basicConfig(level=logging.INFO)

            # print self.logging_level
            # print self.debug_level

    def main(self):

        # TODO multi chain support, start process for each chain within master_chain
        # for i in range(0, procs):
        # r = rocket(self.name, self.chain)

        process = multiprocessing.Process(target=Agent,
                                          args=(self.name, self.mode, self.master_chain,
                                                self.interval, self.logging_level,
                                                self.debug_level))
        self.jobs.append(process)

        for j in self.jobs:
            j.start()

        for j in self.jobs:
            j.join()
