# -*- coding: utf-8 -*-
"""The tellstick bus and components
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

from janitoo.utils import json_dumps, json_loads, HADD_SEP
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

def make_daylight(**kwargs):
    return TellstickDaylight(**kwargs)

def make_magnetic(**kwargs):
    return TellstickMagnetic(**kwargs)

def make_pir(**kwargs):
    return TellstickPir(**kwargs)

def make_remote(**kwargs):
    return TellstickRemote(**kwargs)

class TellstickDevice(JNTComponent):
    """ Provides the interface for a Tellstick device. """

    def __init__(self, bus=None, addr=None, **kwargs):
        """ Constructor.
        """
        oid = kwargs.pop('oid', '%s.device'%OID)
        product_name = kwargs.pop('product_name', "Unknown device")
        product_type = kwargs.pop('product_type', "Tellstick device")
        product_manufacturer = kwargs.pop('product_manufacturer', "Janitoo")
        name = kwargs.pop('name', "Telldus device")
        JNTComponent.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            product_type=product_type,
            product_manufacturer=product_manufacturer,
            **kwargs
        )

    def check_heartbeat(self):
        """Check that the component is 'available'

        """
        node_uuid = self.node.uuid if self.node else None
        logger.debug("[%s] - Check heartbeat for %s (%s)", self.__class__.__name__, self.oid, node_uuid)
        if node_uuid is None:
            return False
        #Bad way to do it but ...
        node_uuid = node_uuid.replace('%s__'%OID,'')
        tdev = self._bus.get_tdev_from_uuid(node_uuid)
        return self._bus.tellstick_get_name(tdev) is not None

class TellstickSwitch(TellstickDevice):
    """ Provides the interface for a Tellstick device. """

    def __init__(self, bus=None, addr=None, **kwargs):
        """ Constructor.
        """
        oid = kwargs.pop('oid', '%s.switch'%OID)
        product_name = kwargs.pop('product_name', "Tellstick switch")
        name = kwargs.pop('name', "Tellstick switch")
        TellstickDevice.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            **kwargs
        )

        uuid="switch"
        self.values[uuid] = self.value_factory['action_switch_binary'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            list_items=['on', 'off'],
            default='off',
            set_data_cb=self.set_switch,
        )
        poll_value = self.values[uuid].create_poll_value(default=300)
        self.values[poll_value.uuid] = poll_value

    def set_switch(self, node_uuid, index, data):
        """Switch On/Off a dimmer
        """
        add_ctrl, add_node = self.node.split_hadd()
        tdev = self._bus.get_tdev_from_hadd(add_node)
        if data == 'on':
            self._bus.tellstick_turnon(tdev)
        elif data == 'off':
            self._bus.tellstick_turnoff(tdev)
        else:
            logger.warning("[%s] - set_switch unknown data : %s", self.__class__.__name__, data)


class TellstickDimmer(TellstickSwitch):
    """ Provides the interface for a Tellstick device. """

    def __init__(self, bus=None, addr=None, **kwargs):
        """ Constructor.
        """
        oid = kwargs.pop('oid', '%s.dimmer'%OID)
        product_name = kwargs.pop('product_name', "Tellstick dimmer")
        name = kwargs.pop('name', "Tellstick dimmer")
        TellstickSwitch.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            **kwargs
        )

        uuid="dim"
        self.values[uuid] = self.value_factory['action_switch_multilevel'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='Dim a dimmer. A byte from 0 to 100',
            label='Level',
            default=0,
            set_data_cb=self.set_dim,
        )
        poll_value = self.values[uuid].create_poll_value(default=300)
        self.values[poll_value.uuid] = poll_value

    def set_dim(self, node_uuid, index, data):
        """Dim a dimmer
        """
        add_ctrl, add_node = self.node.split_hadd()
        tdev = self._bus.get_tdev_from_hadd(add_node)
        if data > 100:
            data = 100
        elif data < 0:
            data = 0
        self._bus.tellstick_dim(tdev, data)

class TellstickShutter(TellstickDevice):
    """ Provides the interface for a Tellstick device. """

    def __init__(self, bus=None, addr=None, **kwargs):
        """ Constructor.
        """
        oid = kwargs.pop('oid', '%s.shutter'%OID)
        product_name = kwargs.pop('product_name', "Tellstick shutter")
        name = kwargs.pop('name', "Tellstick shutter")
        TellstickDevice.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            **kwargs
        )

        uuid="shutter"
        self.values[uuid] = self.value_factory['action_shutter_binary'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            list_items=['up', 'down', 'stop'],
            default='up',
            set_data_cb=self.set_shutter,
        )
        poll_value = self.values[uuid].create_poll_value(default=300)
        self.values[poll_value.uuid] = poll_value

    def set_shutter(self, node_uuid, index, data):
        """Shutter
        """
        add_ctrl, add_node = self.node.split_hadd()
        tdev = self._bus.get_tdev_from_hadd(add_node)
        #We should add the up, down and stop command too
        if data == 'up':
            self._bus.tellstick_up(tdev)
        elif data == 'down':
            self._bus.tellstick_down(tdev)
        elif data == 'stop':
            self._bus.tellstick_stop(tdev)
        else:
            logger.warning("[%s] - set_shutter unknown data : %s", self.__class__.__name__, data)

class TellstickRemote(TellstickDevice):
    """ Provides the interface for a Tellstick device. """

    def __init__(self, bus=None, addr=None, **kwargs):
        """ Constructor.
        """
        oid = kwargs.pop('oid', '%s.remote'%OID)
        product_name = kwargs.pop('product_name', "Tellstick sensor")
        name = kwargs.pop('name', "Tellstick sensor")
        TellstickDevice.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            **kwargs
        )

        uuid="button"
        self.values[uuid] = self.value_factory['action_button_binary'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            list_items=['on', 'off'],
            default='off',
        )
        poll_value = self.values[uuid].create_poll_value(default=300)
        self.values[poll_value.uuid] = poll_value

        uuid="groupe"
        self.values[uuid] = self.value_factory['sensor_integer'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            label="groupe",
            default='off',
            genre=0x01,
        )
        poll_value = self.values[uuid].create_poll_value(default=300)
        self.values[poll_value.uuid] = poll_value

class TellstickBell(TellstickDevice):
    """ Provides the interface for a Tellstick device. """

    def __init__(self, bus=None, addr=None, **kwargs):
        """ Constructor.
        """
        oid = kwargs.pop('oid', '%s.bell'%OID)
        product_name = kwargs.pop('product_name', "Tellstick bell")
        name = kwargs.pop('name', "Tellstick bell")
        TellstickDevice.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            **kwargs
        )
        uuid="button"
        self.values[uuid] = self.value_factory['action_button_binary'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            list_items=['on', 'off'],
            default='off',
        )
        poll_value = self.values[uuid].create_poll_value(default=300)
        self.values[poll_value.uuid] = poll_value

class TellstickSensor(TellstickDevice):
    """ Provides the interface for a Tellstick device. """

    def __init__(self, bus=None, addr=None, **kwargs):
        """ Constructor.
        """
        oid = kwargs.pop('oid', '%s.sensor'%OID)
        product_name = kwargs.pop('product_name', "Tellstick sensor")
        name = kwargs.pop('name', "Tellstick sensor")
        TellstickDevice.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            **kwargs
        )
        uuid="status"
        self.values[uuid] = self.value_factory['sensor_boolean'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The status of the sensor',
            label='Status',
        )
        poll_value = self.values[uuid].create_poll_value(default=60)
        self.values[poll_value.uuid] = poll_value


class TellstickDaylight(TellstickSensor):
    """ Provides the interface for a Tellstick device. """

    def __init__(self, bus=None, addr=None, **kwargs):
        """ Constructor.
        """
        oid = kwargs.pop('oid', '%s.daylight'%OID)
        product_name = kwargs.pop('product_name', "Tellstick daylight")
        name = kwargs.pop('name', "Tellstick daylight")
        TellstickSensor.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            **kwargs
        )

class TellstickMagnetic(TellstickSensor):
    """ Provides the interface for a Tellstick device. """

    def __init__(self, bus=None, addr=None, **kwargs):
        """ Constructor.
        """
        oid = kwargs.pop('oid', '%s.magnetic'%OID)
        product_name = kwargs.pop('product_name', "Tellstick magnetic")
        name = kwargs.pop('name', "Tellstick magnetic")
        TellstickSensor.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            **kwargs
        )

class TellstickPir(TellstickSensor):
    """ Provides the interface for a Tellstick device. """

    def __init__(self, bus=None, addr=None, **kwargs):
        """ Constructor.
        """
        oid = kwargs.pop('oid', '%s.pir'%OID)
        product_name = kwargs.pop('product_name', "Tellstick pir")
        name = kwargs.pop('name', "Tellstick pir")
        TellstickSensor.__init__(self,
            oid=oid,
            bus=bus,
            addr=addr,
            name=name,
            product_name=product_name,
            **kwargs
        )
