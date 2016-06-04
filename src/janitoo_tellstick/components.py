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
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

# Set default logging handler to avoid "No handler found" warnings.
import logging
logger = logging.getLogger(__name__)

from subprocess import PIPE
from janitoo.utils import json_dumps, json_loads
from janitoo.component import JNTComponent

from janitoo_tellstick import OID

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

def make_device(**kwargs):
    return TellstickDevice(**kwargs)

def make_sensor(**kwargs):
    return TellstickSensor(**kwargs)

def make_switch(**kwargs):
    return TellstickSwitch(**kwargs)

def make_dimmer(**kwargs):
    return TellstickDimmer(**kwargs)

def make_shutter(**kwargs):
    return TellstickShutter(**kwargs)

def make_bell(**kwargs):
    return TellstickBell(**kwargs)

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
        oid = kwargs.pop('oid', '%s.device'%OID)
        product_name = kwargs.pop('product_name', "Telldus device")
        product_type = kwargs.pop('product_type', "Telldus device")
        product_manufacturer = kwargs.pop('product_manufacturer', "Janitoo")
        name = kwargs.pop('name', "Telldus device")
        JNTComponent.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            product_type=product_type,
            product_manufacturer=product_manufacturer
        )

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
        oid = kwargs.pop('oid', '%s.sensor'%OID)
        product_name = kwargs.pop('product_name', "Telldus sensor")
        product_type = kwargs.pop('product_type', "Telldus sensor")
        product_manufacturer = kwargs.pop('product_manufacturer', "Janitoo")
        name = kwargs.pop('name', "Telldus sensor")
        JNTComponent.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            product_type=product_type,
            product_manufacturer=product_manufacturer
        )

class TellstickSwitch(JNTComponent):
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
        oid = kwargs.pop('oid', '%s.switch'%OID)
        product_name = kwargs.pop('product_name', "Telldus switch")
        product_type = kwargs.pop('product_type', "Telldus switch")
        product_manufacturer = kwargs.pop('product_manufacturer', "Janitoo")
        name = kwargs.pop('name', "Telldus switch")
        JNTComponent.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            product_type=product_type,
            product_manufacturer=product_manufacturer
        )

class TellstickDimmer(JNTComponent):
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
        oid = kwargs.pop('oid', '%s.dimmer'%OID)
        product_name = kwargs.pop('product_name', "Telldus dimmer")
        product_type = kwargs.pop('product_type', "Telldus dimmer")
        product_manufacturer = kwargs.pop('product_manufacturer', "Janitoo")
        name = kwargs.pop('name', "Telldus dimmer")
        JNTComponent.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            product_type=product_type,
            product_manufacturer=product_manufacturer
        )

class TellstickShutter(JNTComponent):
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
        oid = kwargs.pop('oid', '%s.shutter'%OID)
        product_name = kwargs.pop('product_name', "Telldus shutter")
        product_type = kwargs.pop('product_type', "Telldus shutter")
        product_manufacturer = kwargs.pop('product_manufacturer', "Janitoo")
        name = kwargs.pop('name', "Telldus shutter")
        JNTComponent.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            product_type=product_type,
            product_manufacturer=product_manufacturer
        )

class TellstickBell(JNTComponent):
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
        oid = kwargs.pop('oid', '%s.bell'%OID)
        product_name = kwargs.pop('product_name', "Telldus bell")
        product_type = kwargs.pop('product_type', "Telldus bell")
        product_manufacturer = kwargs.pop('product_manufacturer', "Janitoo")
        name = kwargs.pop('name', "Telldus bell")
        JNTComponent.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            product_type=product_type,
            product_manufacturer=product_manufacturer
        )
