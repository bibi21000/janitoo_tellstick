# -*- coding: utf-8 -*-

"""Unittests for Janitoo-Roomba Server.
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
from janitoo_nosetests.thread import JNTTThreadRun, JNTTThreadRunCommon
from janitoo_nosetests.component import JNTTComponent, JNTTComponentCommon

from janitoo.utils import json_dumps, json_loads
from janitoo.utils import HADD_SEP, HADD
from janitoo.utils import TOPIC_HEARTBEAT
from janitoo.utils import TOPIC_NODES, TOPIC_NODES_REPLY, TOPIC_NODES_REQUEST
from janitoo.utils import TOPIC_BROADCAST_REPLY, TOPIC_BROADCAST_REQUEST
from janitoo.utils import TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC

import telldus

class TestTellstickDuoThread(JNTTThreadRun, JNTTThreadRunCommon):
    """Test the thread
    """
    thread_name = "tellstick"
    conf_file = "tests/data/janitoo_tellstick_duo.conf"

    def test_100_discover_devices(self):
        self.wait_for_nodeman()
        time.sleep(5)
        self.thread.bus.tellstick_discover_new_devices()

    def test_101_event_sensor_callback(self):
        self.wait_for_nodeman()
        time.sleep(5)
        dt = datetime.datetime.now()
        #~ print "values %s", self.thread.bus.values
        self.thread.bus.event_sensor_callback("testproto", 'testmodel', 12, telldus.TELLSTICK_TEMPERATURE, 10, dt, 0)
        print "sensors %s", self.thread.bus.sensors
        self.assertEqual(10, self.thread.bus.sensors["testproto"][12]['temperature']['value'])
        self.assertEqual(dt, self.thread.bus.sensors["testproto"][12]['temperature']['timestamp'])
        self.thread.bus.event_sensor_callback("testproto", 'testmodel', 6, telldus.TELLSTICK_TEMPERATURE, 10, dt, 0)
        print "sensors %s", self.thread.bus.sensors
        self.assertEqual(10, self.thread.bus.sensors["testproto"][6]['temperature']['value'])
        self.assertEqual(dt, self.thread.bus.sensors["testproto"][6]['temperature']['timestamp'])

        self.thread.bus.event_sensor_callback("testproto", 'testmodel', 14, telldus.TELLSTICK_HUMIDITY, 39, dt, 0)
        print "sensors %s", self.thread.bus.sensors
        self.assertEqual(39, self.thread.bus.sensors["testproto"][14]['humidity']['value'])
        self.assertEqual(dt, self.thread.bus.sensors["testproto"][14]['humidity']['timestamp'])

        self.thread.bus.event_sensor_callback("testproto", 'testmodel', 7, telldus.TELLSTICK_RAINTOTAL, 41, dt, 0)
        print "sensors %s", self.thread.bus.sensors
        self.assertEqual(41, self.thread.bus.sensors["testproto"][7]['rain_total']['value'])
        self.assertEqual(dt, self.thread.bus.sensors["testproto"][7]['rain_total']['timestamp'])

        self.thread.bus.event_sensor_callback("testproto", 'testmodel', 18, telldus.TELLSTICK_RAINRATE, 3.2, dt, 0)
        print "sensors %s", self.thread.bus.sensors
        self.assertEqual(3.2, self.thread.bus.sensors["testproto"][18]['rain_rate']['value'])
        self.assertEqual(dt, self.thread.bus.sensors["testproto"][18]['rain_rate']['timestamp'])

        self.assertTrue(False)
