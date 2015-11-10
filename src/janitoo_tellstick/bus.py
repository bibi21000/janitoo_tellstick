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
import time
from datetime import datetime, timedelta
from subprocess import Popen, PIPE
import base64
from subprocess import Popen, PIPE
import re
import socket
from janitoo.thread import JNTThread
from janitoo.options import get_option_autostart
from janitoo.utils import HADD, HADD_SEP, json_dumps, json_loads
from janitoo.node import JNTNode
from janitoo.value import JNTValue
from janitoo.component import JNTComponent
from janitoo.bus import JNTBus
from janitoo.classes import COMMAND_DESC

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_DISPLAY = 0x0061
COMMAND_AV_CHANNEL = 0x2100
COMMAND_AV_VOLUME = 0x2101
COMMAND_NOTIFY = 0x3010

assert(COMMAND_DESC[COMMAND_DISPLAY] == 'COMMAND_DISPLAY')
assert(COMMAND_DESC[COMMAND_AV_CHANNEL] == 'COMMAND_AV_CHANNEL')
assert(COMMAND_DESC[COMMAND_AV_VOLUME] == 'COMMAND_AV_VOLUME')
assert(COMMAND_DESC[COMMAND_NOTIFY] == 'COMMAND_NOTIFY')
##############################################################

def make_duo(**kwargs):
    return TellstickDevice(**kwargs)

def make_device(**kwargs):
    return TellstickDevice(**kwargs)

def make_sensor(**kwargs):
    return TellstickSensor(**kwargs)

class TellstickBus(JNTBus):
    """A pseudo-bus to manage all TVs
    """
    def __init__(self, name='Samsung bus', **kwargs):
        """
        :param int bus_id: the SMBus id (see Raspberry Pi documentation)
        :param kwargs: parameters transmitted to :py:class:`smbus.SMBus` initializer
        """
        JNTBus.__init__(self, 'samsung', name=name, **kwargs)

    @property
    def uuid(self):
        """Return an uuid for the bus

        """
        return "samsung"

class TellstickDevice(JNTComponent):
    """ Provides the interface for a DS18B20 device. """

    def __init__(self, bus=None, addr=None, **kwargs):
        """ Constructor.

        Arguments:
            bus:
                a 1-Wire instance representing the bus this device is
                connected to
            addr:
                the 1-Wire device address (in 7 bits format)
        """
        JNTComponent.__init__(self, 'samsung.ue46', bus=bus, addr=addr, name="UE46xxxs Samsung TVs")
        self.ip = kwargs.get('ip', '192.168.14.50')
        """The IP address of the tv"""
        self.port_cmd = int(kwargs.get('port_cmd', 55000))
        """The port command of the tv"""
        self.port_notif = int(kwargs.get('port_cmd', 52235))
        """The port notification of the tv"""
        self.mac_address = kwargs.get('mac_address', "e4:e0:c5:b3:52:a2")
        """The mac_address of the tv"""
        self.remote_name = kwargs.get('remote_name', "Janitoo Remote Control")
        """The remote_name for the tv"""
        self.ip_source = kwargs.get('ip_source', None)
        """The ip of the remote"""
        self._delay_sleep = 0.05
        """The delay betwenn two commands to the tv"""

        uuid = '%s__%s'%(self.uuid,'channel_change')
        value = JNTValue( uuid=uuid,
                help='Channel change (up=true, down=false)',
                index=0,
                cmd_class=COMMAND_AV_CHANNEL,
                genre=0x02,
                type=0x01,
                set_data_cb=self.channel_change,
                is_writeonly=True,
                )
        self.values[uuid] = value
        uuid = '%s__%s'%(self.uuid,'channel_set')
        value = JNTValue( uuid=uuid,
                help='Channel set',
                index=0,
                cmd_class=COMMAND_AV_CHANNEL,
                genre=0x02,
                type=0x02,
                set_data_cb=self.channel_set,
                is_writeonly=True,
                )
        self.values[uuid] = value
        self.cmd_classes.append(COMMAND_AV_CHANNEL)

    @property
    def uuid(self):
        """Return an uuid for the component

        """
        return "samsung__%s" % (self.ip.replace(HADD_SEP,'').replace(':','').replace('/',''))

    def check_heartbeat(self):
        """Check that the component is 'available'

        """
        try:
            if os.system('ping -c 2 ' + self.ip):
                return False
            return True
        except :
            logger.exception('[%s] - Exception when checking heartbeat of the tv (%s)', self.__class__.__name__, self.ip)

class TellstickSensor(JNTComponent):
    """ Provides the interface for a DS18B20 device. """

    def __init__(self, bus=None, addr=None, **kwargs):
        """ Constructor.

        Arguments:
            bus:
                a 1-Wire instance representing the bus this device is
                connected to
            addr:
                the 1-Wire device address (in 7 bits format)
        """
        JNTComponent.__init__(self, 'samsung.ue46', bus=bus, addr=addr, name="UE46xxxs Samsung TVs")
        self.ip = kwargs.get('ip', '192.168.14.50')
        """The IP address of the tv"""
        self.port_cmd = int(kwargs.get('port_cmd', 55000))
        """The port command of the tv"""
        self.port_notif = int(kwargs.get('port_cmd', 52235))
        """The port notification of the tv"""
        self.mac_address = kwargs.get('mac_address', "e4:e0:c5:b3:52:a2")
        """The mac_address of the tv"""
        self.remote_name = kwargs.get('remote_name', "Janitoo Remote Control")
        """The remote_name for the tv"""
        self.ip_source = kwargs.get('ip_source', None)
        """The ip of the remote"""
        self._delay_sleep = 0.05
        """The delay betwenn two commands to the tv"""

        uuid = '%s__%s'%(self.uuid,'channel_change')
        value = JNTValue( uuid=uuid,
                help='Channel change (up=true, down=false)',
                index=0,
                cmd_class=COMMAND_AV_CHANNEL,
                genre=0x02,
                type=0x01,
                set_data_cb=self.channel_change,
                is_writeonly=True,
                )
        self.values[uuid] = value
        uuid = '%s__%s'%(self.uuid,'channel_set')
        value = JNTValue( uuid=uuid,
                help='Channel set',
                index=0,
                cmd_class=COMMAND_AV_CHANNEL,
                genre=0x02,
                type=0x02,
                set_data_cb=self.channel_set,
                is_writeonly=True,
                )
        self.values[uuid] = value
        self.cmd_classes.append(COMMAND_AV_CHANNEL)

    @property
    def uuid(self):
        """Return an uuid for the component

        """
        return "samsung__%s" % (self.ip.replace(HADD_SEP,'').replace(':','').replace('/',''))

    def check_heartbeat(self):
        """Check that the component is 'available'

        """
        try:
            if os.system('ping -c 2 ' + self.ip):
                return False
            return True
        except :
            logger.exception('[%s] - Exception when checking heartbeat of the tv (%s)', self.__class__.__name__, self.ip)

