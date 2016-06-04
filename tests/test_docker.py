# -*- coding: utf-8 -*-

"""Unittests for Janitoo-common.
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
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

import warnings
warnings.filterwarnings("ignore")

import sys, os
import time
import unittest
import logging
import threading
import mock
import logging

from janitoo_nosetests import JNTTBase
from janitoo_nosetests.server import JNTTDockerServerCommon, JNTTDockerServer

from janitoo.runner import Runner, jnt_parse_args
from janitoo.server import JNTServer
from janitoo.utils import HADD_SEP, HADD

class TestTellstickDuoSerser(JNTTDockerServerCommon, JNTTDockerServer):
    """Test the server
    """
    loglevel = logging.DEBUG
    path = '/tmp/janitoo_test'
    broker_user = 'toto'
    broker_password = 'toto'
    server_class = JNTServer
    server_conf = "tests/data/janitoo_tellstick.conf"
    server_section = "tellstick"
    hadds = [HADD%(163,0)]

class TestTellstickDuoSerser(JNTTDockerServerCommon, JNTTDockerServer):
    """Test the server
    """
    loglevel = logging.DEBUG
    path = '/tmp/janitoo_test'
    broker_user = 'toto'
    broker_password = 'toto'
    server_class = JNTServer
    server_conf = "tests/data/janitoo_tellstick_duo.conf"
    server_section = "tellstick"
    hadds = [HADD%(163,0)]

    def test_100_discover_devices(self):
        self.start()
        time.sleep(10)
        thread = self.server.find_thread(self.server_section)
        self.assertNotEqual(thread, None)
        self.assertIsInstance(thread, JNTBusThread)
        bus = thread.bus
        self.assertNotEqual(bus, None)
        self.waitHeartbeatNodes(hadds=self.hadds)
        bus.tellstick_discover_new_devices()
        time.sleep(30)
