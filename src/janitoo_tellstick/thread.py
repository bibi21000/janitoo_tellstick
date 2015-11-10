# -*- coding: utf-8 -*-
"""The Roomba Janitoo helper
It handle all communications to the Roomba vacuum



"""

__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015 Sébastien GALLET aka bibi21000"

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+                                   # pragma: no cover
    from logging import NullHandler                   # pragma: no cover
except ImportError:                                   # pragma: no cover
    class NullHandler(logging.Handler):               # pragma: no cover
        """NullHandler logger for python 2.6"""       # pragma: no cover
        def emit(self, record):                       # pragma: no cover
            pass                                      # pragma: no cover
logger = logging.getLogger('janitoo.roomba')
import os, sys
import threading
import requests
from datetime import datetime, timedelta
from janitoo.thread import JNTThread
from janitoo.options import get_option_autostart
from janitoo.utils import HADD, json_dumps, json_loads
from janitoo.node import JNTNode
from janitoo.value import JNTValue
from bus import TellstickBus

def make_thread(options):
    if get_option_autostart(options, 'samsung') == True:
        return TellstickThread(options)
    else:
        return None

class TellstickThread(JNTThread):
    """The Tellstick thread

    """
    def boot(self):
        """configure the HADD address
        """
        self.add_ctrl = 56
        self.hadds = { 0 : HADD%(self.add_ctrl,0),
                       'tv1' : HADD%(self.add_ctrl,1),
                       'tv2' : HADD%(self.add_ctrl,2),
                     }

    def pre_loop(self):
        """Pre-Run the loop
        """
        self._tellstick_bus = TellstickBus(options=self.options)
        settings = self.get_settings('samsung')
        self.apply_settings(self._tellstick_bus, settings)
        self._tellstick_bus.start(self.mqtt_nodes, self.trigger_reload)
        components = self.get_components('samsung')
        self.build_bus_components('samsung', components, self._tellstick_bus)
        logger.info('Load %s component(s)', len(components))

    def post_loop(self):
        """Post-Run the loop
        """
        if self._tellstick_bus != None:
            self._tellstick_bus.stop()
        self._tellstick_bus = None

