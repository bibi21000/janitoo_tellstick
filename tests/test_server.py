# -*- coding: utf-8 -*-

"""Unittests for Janitoo Server.
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
import time, datetime
import unittest
import threading
import logging
from pkg_resources import iter_entry_points

from janitoo_nosetests.server import JNTTServer, JNTTServerCommon

from janitoo.utils import json_dumps, json_loads
from janitoo.utils import HADD_SEP, HADD
from janitoo.utils import TOPIC_HEARTBEAT
from janitoo.utils import TOPIC_NODES, TOPIC_NODES_REPLY, TOPIC_NODES_REQUEST
from janitoo.utils import TOPIC_BROADCAST_REPLY, TOPIC_BROADCAST_REQUEST
from janitoo.utils import TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC

from janitoo.thread import JNTBusThread

from janitoo.server import JNTServer

#~ class TestTellstickSerser(JNTTServer, JNTTServerCommon):
    #~ """Test the server
    #~ """
    #~ loglevel = logging.DEBUG
    #~ path = '/tmp/janitoo_test'
    #~ broker_user = 'toto'
    #~ broker_password = 'toto'
    #~ server_class = JNTServer
    #~ server_conf = "tests/data/janitoo_tellstick.conf"
    #~ server_section = "tellstick"
    #~ hadds = [HADD%(163,0)]

class TestTellstickDuoSerser(JNTTServer, JNTTServerCommon):
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

    def test_101_update_device_components(self):
        self.skipManualTest("Only on my installation")
        self.start()
        time.sleep(10)
        thread = self.server.find_thread(self.server_section)
        self.assertNotEqual(thread, None)
        self.assertIsInstance(thread, JNTBusThread)
        bus = thread.bus
        self.assertNotEqual(bus, None)
        self.waitHeartbeatNodes(hadds=self.hadds)
        time.sleep(10)
        bus.tellstick_update_device_component('0163/0007', 'tellstick.switch')
        bus.tellstick_update_device_component('0163/0005', 'tellstick.shutter')

#~ class TestTellstickNetSerser(JNTTServer, JNTTServerCommon):
    #~ """Test the server
    #~ """
    #~ loglevel = logging.DEBUG
    #~ path = '/tmp/janitoo_test'
    #~ broker_user = 'toto'
    #~ broker_password = 'toto'
    #~ server_class = JNTServer
    #~ server_conf = "tests/data/janitoo_tellstick_net.conf"
    #~ server_section = "tellstick"
    #~ hadds = [HADD%(163,0)]
