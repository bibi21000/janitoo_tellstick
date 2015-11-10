# -*- coding: utf-8 -*-

"""The Samsung server

See http://www.roowifi.com/sample-python-gtk/
See https://github.com/maxvitek/roowifi
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

from threading import Thread, Event
import subprocess
import time
import traceback
import urllib
import socket
import urllib2
import json
import requests
import json
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
#logger.addHandler(NullHandler())

from pkg_resources import get_distribution, DistributionNotFound
from janitoo.mqtt import MQTTClient
from janitoo.server import JNTServer


class TellstickServer(JNTServer):
    """The Tellstick Server

    """
    def _get_egg_path(self):
        """Return the egg path of the module. Must be redefined in server class. Used to find alembic migration scripts.
        """
        try:
            _dist = get_distribution('janitoo_samsung')
            return _dist.__file__
        except AttributeError:
            return 'src-samsung/config'

