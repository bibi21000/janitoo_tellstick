# -*- coding: utf-8 -*-
"""The Raspberry tellstick bus
Warning : this bus can't be aggregate/ Need to run in its own thread.
Not sure that this bus can be extended by aggregation (callbacks and constants : TELLSTICK_TEMPERATURE).
Need to be tested.

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

import threading
import time

from janitoo.bus import JNTBus
from janitoo.utils import HADD

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_CAMERA_PREVIEW = 0x2200
COMMAND_CAMERA_PHOTO = 0x2201
COMMAND_CAMERA_VIDEO = 0x2202
COMMAND_CAMERA_STREAM = 0x2203

assert(COMMAND_DESC[COMMAND_CAMERA_PREVIEW] == 'COMMAND_CAMERA_PREVIEW')
assert(COMMAND_DESC[COMMAND_CAMERA_PHOTO] == 'COMMAND_CAMERA_PHOTO')
assert(COMMAND_DESC[COMMAND_CAMERA_VIDEO] == 'COMMAND_CAMERA_VIDEO')
assert(COMMAND_DESC[COMMAND_CAMERA_STREAM] == 'COMMAND_CAMERA_STREAM')
##############################################################

from janitoo_tellstick import OID

class TellstickBus(JNTBus):
    """A pseudo-bus to handle the tellstick
    """

    # Commands
    TELLSTICK_TURNON = 1
    TELLSTICK_TURNOFF = 2
    TELLSTICK_BELL = 4
    TELLSTICK_TOGGLE = 8
    TELLSTICK_DIM = 16
    TELLSTICK_LEARN = 32
    TELLSTICK_EXECUTE = 64
    TELLSTICK_UP = 128
    TELLSTICK_DOWN = 256
    TELLSTICK_STOP = 512
    ALL_METHODS = TELLSTICK_TURNON | TELLSTICK_TURNOFF | TELLSTICK_BELL | \
                       TELLSTICK_DIM | TELLSTICK_UP | TELLSTICK_DOWN | \
                       TELLSTICK_STOP

    #Sensors
    TELLSTICK_TEMPERATURE = 1
    TELLSTICK_HUMIDITY = 2
    TELLSTICK_RAINRATE = 4
    TELLSTICK_RAINTOTAL = 8
    TELLSTICK_WINDDIRECTION = 16
    TELLSTICK_WINDAVERAGE = 32
    TELLSTICK_WINDGUST = 64

    # Error codes
    TELLSTICK_SUCCESS = 0
    TELLSTICK_ERROR_NOT_FOUND = -1
    TELLSTICK_ERROR_PERMISSION_DENIED = -2
    TELLSTICK_ERROR_DEVICE_NOT_FOUND = -3
    TELLSTICK_ERROR_METHOD_NOT_SUPPORTED = -4
    TELLSTICK_ERROR_COMMUNICATION = -5
    TELLSTICK_ERROR_CONNECTING_SERVICE = -6
    TELLSTICK_ERROR_UNKNOWN_RESPONSE = -7
    TELLSTICK_ERROR_SYNTAX = -8
    TELLSTICK_ERROR_BROKEN_PIPE = -9
    TELLSTICK_ERROR_COMMUNICATING_SERVICE = -10
    TELLSTICK_ERROR_CONFIG_SYNTAX = -11
    TELLSTICK_ERROR_UNKNOWN = -99

    # Controller typedef
    TELLSTICK_CONTROLLER_TELLSTICK = 1
    TELLSTICK_CONTROLLER_TELLSTICK_DUO = 2
    TELLSTICK_CONTROLLER_TELLSTICK_NET = 3

    # Device typedef
    TELLSTICK_TYPE_DEVICE = 1
    TELLSTICK_TYPE_GROUP = 2
    TELLSTICK_TYPE_SCENE = 3

    # Device changes
    TELLSTICK_DEVICE_ADDED = 1
    TELLSTICK_DEVICE_CHANGED = 2
    TELLSTICK_DEVICE_REMOVED = 3
    TELLSTICK_DEVICE_STATE_CHANGED = 4

    # Change types
    TELLSTICK_CHANGE_NAME = 1
    TELLSTICK_CHANGE_PROTOCOL = 2
    TELLSTICK_CHANGE_MODEL = 3
    TELLSTICK_CHANGE_METHOD = 4
    TELLSTICK_CHANGE_AVAILABLE = 5
    TELLSTICK_CHANGE_FIRMWARE = 6

    def __init__(self, **kwargs):
        """
        :param int bus_id: the SMBus id (see Raspberry Pi documentation)
        :param kwargs: parameters transmitted to :py:class:`smbus.SMBus` initializer
        """
        JNTBus.__init__(self, **kwargs)
        self._tellstick_lock = threading.Lock()
        self._lock_delay = 0.5

        self.load_extensions(OID)
        self.cant_aggregate(OID)

        self.sensors = {}
        #~ self.export_attrs('tellstick_acquire', self.tellstick_acquire)
        #~ self.export_attrs('tellstick_release', self.tellstick_release)
        #~ self.export_attrs('tellstick_locked', self.tellstick_locked)
        #~ self.export_attrs('tellstick_turnon', self.tellstick_turnon)
        #~ self.export_attrs('tellstick_turnoff', self.tellstick_turnoff)
        #~ self.export_attrs('tellstick_dim', self.tellstick_dim)
        #~ self.export_attrs('tellstick_bell', self.tellstick_bell)
        #~ self.export_attrs('tellstick_execute', self.tellstick_execute)
        #~ self.export_attrs('tellstick_up', self.tellstick_up)
        #~ self.export_attrs('tellstick_down', self.tellstick_down)
        #~ self.export_attrs('tellstick_stop', self.tellstick_stop)

    def tellstick_turnon(tdev):
        """Turn on a telldus device"""
        pass

    def tellstick_turnoff(tdev):
        """Turn off a telldus device"""
        pass

    def tellstick_dim(tdev, level):
        """Dim a telldus device. Level from 0 to 255."""
        pass

    def tellstick_learn(tdev):
        """Learn a telldus device."""
        pass

    def tellstick_bell(tdev):
        """Bell a telldus device."""
        pass

    def tellstick_execute(tdev):
        """Execute a scene action."""
        pass

    def tellstick_up(tdev):
        """Up a telldus device."""
        pass

    def tellstick_down(tdev):
        """Down a telldus device."""
        pass

    def tellstick_stop(tdev):
        """Stop a telldus device."""
        pass

    def tellstick_resend(tdev):
        """Resend last command to a telldus device."""
        pass

    def tellstick_acquire(self, blocking=True):
        """Get a lock on the bus"""
        if self._tellstick_lock.acquire(blocking):
            return True
        return False

    def tellstick_release(self):
        """Release a lock on the bus"""
        self._tellstick_lock.release()

    def tellstick_locked(self):
        """Get status of the lock"""
        return self._tellstick_lock.locked()

def extend_duo( self ):
    import telldus
    telldus.tdInit()


    def set_tellstickduo_discover(node_uuid, index, data):
        """
        """
        if data:
            self._bus.tellstick_discover_new_devices()
        else:
            logger.warning("[%s] - set_tellstickduo_discover unknown data : %s", self.__class__.__name__, data)
        return True
    self.set_tellstickduo_discover = set_tellstickduo_discover
    uuid="{:s}_discover".format(self.oid)
    self.values[uuid] = self.value_factory['action_boolean'](options=self.options, uuid=uuid,
        node_uuid=self.uuid,
        set_data_cb=self.set_tellstickduo_discover,
    )


    def set_tellstickduo_updatetype(node_uuid, index, data):
        """
        """
        if data:
            self._bus.tellstick_update_device_component(node_uuid, data)
        else:
            logger.warning("[%s] - set_tellstickduo_discover unknown data : %s", self.__class__.__name__, data)
        return True
    self.set_tellstickduo_updatetype = set_tellstickduo_updatetype
    uuid="{:s}_updatetype".format(self.oid)
    self.values[uuid] = self.value_factory['action_string'](options=self.options, uuid=uuid,
        node_uuid=self.uuid,
        set_data_cb=self.set_tellstickduo_updatetype,
    )


    def get_hadd_from_tdev(tdev):
        """
        """
        return tdev+1
    self.get_hadd_from_tdev = get_hadd_from_tdev

    def get_uuid_from_tdev(tdev):
        """
        """
        return tdev+1
    self.get_uuid_from_tdev = get_uuid_from_tdev

    def get_tdev_from_hadd(hadd):
        """
        """
        hadd = int(hadd)
        return hadd-1
    self.get_tdev_from_hadd = get_tdev_from_hadd

    def get_tdev_from_uuid(uuid):
        """
        """
        hadd = int(uuid)
        return hadd-1
    self.get_tdev_from_uuid = get_tdev_from_uuid


    def event_device_change_callback(device_id, change_event, change_type, callback_id, context):
        """
        """
        logger.debug("[%s] - Receive change %s callback for %s", self.__class__.__name__,change_event , device_id)
        return True
    self.event_device_change_callback = event_device_change_callback
    self.event_change_device = telldus.tdRegisterDeviceChangeEvent(self.event_device_change_callback)
    #~ self.export_attrs('event_change_device', self.event_change_device)

    def event_device_callback(device_id, method, value, callback_id):
        """Get an event for a well known device
        """
        uuid = self.get_hadd_from_tdev(device_id)
        logger.debug("[%s] - Receive callback from %s for node %s", self.__class__.__name__, device_id, uuid)
        status = self.nodeman.find_value(uuid, 'status')
        if status is not None:
            #It's a sensor
            if method & self.TELLSTICK_TURNON:
                status.data = True
                self.nodeman.publish_value(status)
                return True
            elif method & self.TELLSTICK_TURNOFF:
                status.data = False
                self.nodeman.publish_value(status)
                return True
        else:
            dim = self.nodeman.find_value(uuid, 'dim')
            if dim is not None:
                #It's a dimmer
                switch = self.nodeman.find_value(uuid, 'switch')
                dimval = 1.0*value/2.55
                if method & self.TELLSTICK_TURNON:
                    switch._data = True
                    self.nodeman.publish_value(switch)
                    return True
                elif method & self.TELLSTICK_TURNOFF:
                    switch._data = False
                    self.nodeman.publish_value(switch)
                    return True
                elif method & self.TELLSTICK_DIM:
                    dim._data = dimval
                    self.nodeman.publish_value(dim)
                    return True
            else:
                shutter = self.nodeman.find_value(uuid, 'shutter')
                if shutter is not None:
                    #It's a shutter
                    if (method & self.TELLSTICK_TURNON) or (method & self.TELLSTICK_UP):
                        shutter._data = 'up'
                        self.nodeman.publish_value(shutter)
                        return True
                    elif (method & self.TELLSTICK_TURNOFF) or (method & self.TELLSTICK_DOWN):
                        shutter._data = 'down'
                        self.nodeman.publish_value(shutter)
                        return True
                    elif (method & self.TELLSTICK_STOP):
                        shutter._data = 'stop'
                        self.nodeman.publish_value(shutter)
                        return True
                else:
                    button = self.nodeman.find_value(uuid, 'button')
                    if button is not None:
                        #It's a remote or a bell
                        if (method & self.TELLSTICK_TURNON):
                            button.data = 'on'
                            self.nodeman.publish_value(button)
                            return True
                        elif (method & self.TELLSTICK_TURNOFF):
                            button.data = 'off'
                            self.nodeman.publish_value(button)
                            return True
                    else:
                        switch = self.nodeman.find_value(uuid, 'switch')
                        if switch is not None:
                            #It's a switch
                            if (method & self.TELLSTICK_TURNON):
                                switch._data = 'on'
                                self.nodeman.publish_value(switch)
                                return True
                            elif (method & self.TELLSTICK_TURNOFF):
                                switch._data = 'off'
                                self.nodeman.publish_value(switch)
                                return True
        logger.warning("[%s] - Receive callback from %s but node %s didn't process message %s (%s)", self.__class__.__name__, device_id, uuid, method, value)
        return False
    self.event_device_callback = event_device_callback
    self.event_device = telldus.tdRegisterDeviceEvent(self.event_device_callback)
    #~ self.export_attrs('event_device', self.event_device)


    def get_temperature(node_uuid, index):
        """Get the temperature sensors
        """
        return 0
    self.get_temperature = get_temperature

    uuid="{:s}_temperature".format(OID)
    self.values[uuid] = self.value_factory['sensor_temperature'](options=self.options, uuid=uuid,
        node_uuid=self.uuid,
        get_data_cb=self.get_temperature,
        help='The temperature sensors.',
        label='Temp',
    )
    poll_value = self.values[uuid].create_poll_value(default=300)
    self.values[poll_value.uuid] = poll_value
    config_value = self.values[uuid].create_config_value(type=0x16, help='The sensor ids', default="")
    self.values[config_value.uuid] = config_value


    def get_humidity(node_uuid, index):
        """Get the humidity sensors
        """
        return 0
    self.get_humidity = get_humidity

    uuid="{:s}_humidity".format(OID)
    self.values[uuid] = self.value_factory['sensor_humidity'](options=self.options, uuid=uuid,
        node_uuid=self.uuid,
        get_data_cb=self.get_humidity,
        help='The humidity sensors.',
        label='Hum',
    )
    poll_value = self.values[uuid].create_poll_value(default=300)
    self.values[poll_value.uuid] = poll_value
    config_value = self.values[uuid].create_config_value(type=0x16, help='The sensor ids', default="")
    self.values[config_value.uuid] = config_value


    def get_rain_rate(node_uuid, index):
        """Get the rain rate sensors
        """
        return 0
    self.get_rain_rate = get_rain_rate

    uuid="{:s}_rain_rate".format(OID)
    self.values[uuid] = self.value_factory['sensor_rain_rate'](options=self.options, uuid=uuid,
        node_uuid=self.uuid,
        get_data_cb=self.get_rain_rate,
        help='The rain rate sensors.',
        label='Rain rate',
    )
    poll_value = self.values[uuid].create_poll_value(default=300)
    self.values[poll_value.uuid] = poll_value
    config_value = self.values[uuid].create_config_value(type=0x16, help='The sensor ids', default="")
    self.values[config_value.uuid] = config_value


    def get_rain_total(node_uuid, index):
        """Get the rain total sensors
        """
        return 0
    self.get_rain_total = get_rain_total

    uuid="{:s}_rain_total".format(OID)
    self.values[uuid] = self.value_factory['sensor_rain_total'](options=self.options, uuid=uuid,
        node_uuid=self.uuid,
        get_data_cb=self.get_rain_total,
        help='The rain total sensors.',
        label='Rain total',
    )
    poll_value = self.values[uuid].create_poll_value(default=300)
    self.values[poll_value.uuid] = poll_value
    config_value = self.values[uuid].create_config_value(type=0x16, help='The sensor ids', default="")
    self.values[config_value.uuid] = config_value


    def get_wind_direction(node_uuid, index):
        """Get the wind direction sensors
        """
        return 0
    self.get_wind_direction = get_wind_direction

    uuid="{:s}_wind_direction".format(OID)
    self.values[uuid] = self.value_factory['sensor_wind_direction'](options=self.options, uuid=uuid,
        node_uuid=self.uuid,
        get_data_cb=self.get_wind_direction,
        help='The wind direction sensors.',
        label='Wind dir',
    )
    poll_value = self.values[uuid].create_poll_value(default=300)
    self.values[poll_value.uuid] = poll_value
    config_value = self.values[uuid].create_config_value(type=0x16, help='The sensor ids', default="")
    self.values[config_value.uuid] = config_value


    def get_wind_average(node_uuid, index):
        """Get the wind average sensors
        """
        return 0
    self.get_wind_average = get_wind_average

    uuid="{:s}_wind_average".format(OID)
    self.values[uuid] = self.value_factory['sensor_wind_average'](options=self.options, uuid=uuid,
        node_uuid=self.uuid,
        get_data_cb=self.get_wind_average,
        help='The wind average sensors.',
        label='Wind avg',
    )
    poll_value = self.values[uuid].create_poll_value(default=300)
    self.values[poll_value.uuid] = poll_value
    config_value = self.values[uuid].create_config_value(type=0x16, help='The sensor ids', default="")
    self.values[config_value.uuid] = config_value


    def get_wind_gust(node_uuid, index):
        """Get the wind gust sensors
        """
        return 0
    self.get_wind_gust = get_wind_gust

    uuid="{:s}_wind_gust".format(OID)
    self.values[uuid] = self.value_factory['sensor_wind_gust'](options=self.options, uuid=uuid,
        node_uuid=self.uuid,
        get_data_cb=self.get_wind_gust,
        help='The wind gust sensors.',
        label='Wind gust',
    )
    poll_value = self.values[uuid].create_poll_value(default=300)
    self.values[poll_value.uuid] = poll_value
    config_value = self.values[uuid].create_config_value(type=0x16, help='The sensor ids')
    self.values[config_value.uuid] = config_value

    def event_sensor_callback(protocol, model, sensor_id, dtype, value, timestamp, callback_id):
        """
        """

        def update_config(which='temperature', protocol='fineoffset'):
            conf = self.get_bus_value("%s_config"%which)
            sensors = [ s for s in conf.data.split('|') if s != '' ]
            print "sensors", sensors
            if '%s'%sensor_id not in sensors:
                lsens = sensors + ['%s'%sensor_id]
                print "lsens", lsens
                conf.data = '|'.join(lsens) if len(lsens)>1 else '%s'%lsens[0]

        if protocol not in self.sensors:
            self.sensors[protocol] = {}
        if sensor_id not in self.sensors[protocol]:
            self.sensors[protocol][sensor_id] = {'model':model}
        if dtype & self.TELLSTICK_TEMPERATURE:
            self.sensors[protocol][sensor_id]['temperature'] = {'value':value, 'timestamp':timestamp}
            update_config(which='temperature', protocol=protocol)
        elif dtype & self.TELLSTICK_HUMIDITY:
            self.sensors[protocol][sensor_id]['humidity'] = {'value':value, 'timestamp':timestamp}
            update_config(which='humidity', protocol=protocol)
        elif dtype & self.TELLSTICK_RAINRATE:
            self.sensors[protocol][sensor_id]['rain_rate'] = {'value':value, 'timestamp':timestamp}
            update_config(which='rain_rate', protocol=protocol)
        elif dtype & self.TELLSTICK_RAINTOTAL:
            self.sensors[protocol][sensor_id]['rain_total'] = {'value':value, 'timestamp':timestamp}
            update_config(which='rain_total', protocol=protocol)
        elif dtype & self.TELLSTICK_WINDDIRECTION:
            self.sensors[protocol][sensor_id]['wind_direction'] = {'value':value, 'timestamp':timestamp}
            update_config(which='wind_direction', protocol=protocol)
        elif dtype & self.TELLSTICK_WINDAVERAGE:
            self.sensors[protocol][sensor_id]['wind_average'] = {'value':value, 'timestamp':timestamp}
            update_config(which='wind_average', protocol=protocol)
        elif dtype & self.TELLSTICK_WINDGUST:
            self.sensors[protocol][sensor_id]['wind_gust'] = {'value':value, 'timestamp':timestamp}
            update_config(which='wind_gust', protocol=protocol)
        else:
            logger.warning("[%s] - Receive unknown sensor event from %s on protocol %s of type %s", self.__class__.__name__, sensor_id, protocol, dtype)
        logger.debug("[%s] - Sensors %s", self.__class__.__name__, self.sensors)
        return True
    self.event_sensor_callback = event_sensor_callback
    self.event_sensor = telldus.tdRegisterSensorEvent(self.event_sensor_callback)
    #~ self.export_attrs('event_sensor', self.event_sensor)


    self._telldusduo_del__ = self.__del__
    def __del__():
        """stop the bus"""
        logger.debug("[%s] - __del__ the bus %s", self.__class__.__name__, self.oid )
        try:
            if self.event_sensor is not None:
                telldus.tdUnregisterCallback(self.event_sensor)
                self.event_sensor = None
                #~ self.export_attrs('event_sensor', self.event_sensor)
        except Exception:
            logger.exception('[%s] - Exception when __del__ bus %s', self.__class__.__name__, self.oid)
        try:
            if self.event_change_device is not None:
                telldus.tdUnregisterCallback(self.event_change_device)
                self.event_change_device = None
                #~ self.export_attrs('event_change_device', self.event_change_device)
        except Exception:
            logger.exception('[%s] - Exception when __del__ bus %s', self.__class__.__name__, self.oid)
        try:
            if self.event_device is not None:
                telldus.tdUnregisterCallback(self.event_device)
                self.event_device = None
                #~ self.export_attrs('event_device', self.event_device)
        except Exception:
            logger.exception('[%s] - Exception when __del__ bus %s', self.__class__.__name__, self.oid)
        try:
            telldus.tdClose()
        except Exception:
            logger.exception('[%s] - Exception when __del__ bus %s', self.__class__.__name__, self.oid)
        return self._telldusduo_del__()
    self.__del__ = __del__

    def tellstick_turnon(tdev):
        """Turn on a telldus device"""
        self.tellstick_acquire()
        try:
            methods = telldus.tdMethods(tdev, self.ALL_METHODS)
            if methods & self.TELLSTICK_TURNON:
                telldus.tdTurnOn(tdev)
                time.sleep(self._lock_delay)
        except Exception:
            logger.exception('[%s] - Exception when tellstick_turnon', self.__class__.__name__)
        finally:
            self.tellstick_release()
    self.tellstick_turnon = tellstick_turnon

    def tellstick_turnoff(tdev):
        """Turn off a telldus device"""
        self.tellstick_acquire()
        try:
            methods = telldus.tdMethods(tdev, self.ALL_METHODS)
            if methods & self.TELLSTICK_TURNOFF:
                telldus.tdTurnOff(tdev)
                time.sleep(self._lock_delay)
        except Exception:
            logger.exception('[%s] - Exception when tellstick_turnoff', self.__class__.__name__)
        finally:
            self.tellstick_release()
    self.tellstick_turnoff = tellstick_turnoff

    def tellstick_dim(tdev, level):
        """Dim a telldus device. Level from 0 to 100."""
        self.tellstick_acquire()
        try:
            methods = telldus.tdMethods(tdev, self.ALL_METHODS)
            if methods & self.TELLSTICK_TURNDIM:
                telldus.tdDim(tdev, int(level*2.55))
                time.sleep(self._lock_delay)
        except Exception:
            logger.exception('[%s] - Exception when tellstick_dim', self.__class__.__name__)
        finally:
            self.tellstick_release()
    self.tellstick_dim = tellstick_dim

    def tellstick_execute(tdev, level):
        """execute a telldus device."""
        self.tellstick_acquire()
        try:
            methods = telldus.tdMethods(tdev, self.ALL_METHODS)
            if methods & self.TELLSTICK_EXECUTE:
                telldus.tdExecute(tdev)
                time.sleep(self._lock_delay)
        except Exception:
            logger.exception('[%s] - Exception when tellstick_execute', self.__class__.__name__)
        finally:
            self.tellstick_release()
    self.tellstick_execute = tellstick_execute

    def tellstick_resend(tdev):
        """Resend last command to a telldus device."""
        self.tellstick_acquire()
        try:
            methods = telldus.tdLastSentCommand(tdev, self.ALL_METHODS)
            if methods & self.TELLSTICK_TURNON:
                telldus.tdTurnOn(tdev)
                time.sleep(self._lock_delay)
            elif methods & self.TELLSTICK_TURNOFF:
                telldus.tdTurnOff(tdev)
                time.sleep(self._lock_delay)
            else:
                logger.warning('[%s] - Unknown resend method %s', self.__class__.__name__, methods)
        except Exception:
            logger.exception('[%s] - Exception when tellstick_up', self.__class__.__name__)
        finally:
            self.tellstick_release()
    self.tellstick_resend = tellstick_resend

    def tellstick_up(tdev):
        """up a telldus device."""
        self.tellstick_acquire()
        try:
            methods = telldus.tdMethods(tdev, self.ALL_METHODS)
            if methods & self.TELLSTICK_UP:
                telldus.tdUp(tdev)
                time.sleep(self._lock_delay)
            elif methods & self.TELLSTICK_TURNON:
                #Emulate up by turnon
                self.tellstick_turnon(tdev)
                time.sleep(self._lock_delay)
        except Exception:
            logger.exception('[%s] - Exception when tellstick_up', self.__class__.__name__)
        finally:
            self.tellstick_release()
    self.tellstick_up = tellstick_up

    def tellstick_down(tdev):
        """down a telldus device. Level from 0 to 255."""
        self.tellstick_acquire()
        try:
            methods = telldus.tdMethods(tdev, self.ALL_METHODS)
            if methods & self.TELLSTICK_DOWN:
                telldus.tdDown(tdev)
                time.sleep(self._lock_delay)
            elif methods & self.TELLSTICK_TURNOFF:
                #Emulate down by turnoff
                self.tellstick_turnoff(tdev)
                time.sleep(self._lock_delay)
        except Exception:
            logger.exception('[%s] - Exception when tellstick_down', self.__class__.__name__)
        finally:
            self.tellstick_release()
    self.tellstick_down = tellstick_down

    def tellstick_stop(tdev):
        """stop a telldus device. Level from 0 to 255."""
        self.tellstick_acquire()
        try:
            methods = telldus.tdMethods(tdev, self.ALL_METHODS)
            if methods & self.TELLSTICK_STOP:
                telldus.tdStop(tdev)
                time.sleep(self._lock_delay)
            elif methods & self.TELLSTICK_TURNOFF or methods & self.TELLSTICK_TURNON:
                #Emulate stop by resending
                self.tellstick_resend(tdev)
                time.sleep(self._lock_delay)
        except Exception:
            logger.exception('[%s] - Exception when tellstick_stop', self.__class__.__name__)
        finally:
            self.tellstick_release()
    self.tellstick_stop = tellstick_stop

    def tellstick_bell(tdev):
        """bell a telldus device."""
        self.tellstick_acquire()
        try:
            methods = telldus.tdMethods(tdev, self.ALL_METHODS)
            if methods & self.TELLSTICK_BELL:
                telldus.tdBell(tdev)
                time.sleep(self._lock_delay)
        except Exception:
            logger.exception('[%s] - Exception when tellstick_bell', self.__class__.__name__)
        finally:
            self.tellstick_release()
    self.tellstick_bell = tellstick_bell

    def tellstick_learn(tdev):
        """learn a telldus device."""
        self.tellstick_acquire()
        try:
            methods = telldus.tdMethods(tdev, self.ALL_METHODS)
            if methods & self.TELLSTICK_LEARN:
                telldus.tdLearn(tdev)
                time.sleep(self._lock_delay)
        except Exception:
            logger.exception('[%s] - Exception when tellstick_learn', self.__class__.__name__)
        finally:
            self.tellstick_release()
    self.tellstick_learn = tellstick_learn

    def tellstick_get_name(tdev):
        """Get the name of telldus device."""
        try:
            return telldus.tdGetName(tdev)
        except Exception:
            logger.exception('[%s] - Exception when tellstick_get_name', self.__class__.__name__)
    self.tellstick_get_name = tellstick_get_name

    def tellstick_discover_new_devices():
        """Discover new devices."""
        devices = telldus.tdGetNumberOfDevices()
        logger.debug('[%s] - Found %s devices in telldus-core', self.__class__.__name__, devices)
        add_ctrl = self.nodeman.get_add_ctrl()
        for i in xrange(devices):
            deviceid = telldus.tdGetDeviceId(i)
            if deviceid:
                name = telldus.tdGetName(deviceid)
                methods = telldus.tdMethods(deviceid, self.ALL_METHODS)
                logger.debug('[%s] - Found device id %s (%s) of type %s with methods : (%s : %s) (%s : %s) (%s : %s) (%s : %s) (%s : %s) (%s : %s) (%s : %s) (%s : %s)',
                    self.__class__.__name__,
                    deviceid, name, telldus.tdGetDeviceType(deviceid),
                    'TELLSTICK_TURNON', methods & self.TELLSTICK_TURNON,
                    'TELLSTICK_TURNOFF', methods & self.TELLSTICK_TURNOFF,
                    'TELLSTICK_DIM', methods & self.TELLSTICK_DIM,
                    'TELLSTICK_BELL', methods & self.TELLSTICK_BELL,
                    'TELLSTICK_EXECUTE', methods & self.TELLSTICK_EXECUTE,
                    'TELLSTICK_UP', methods & self.TELLSTICK_UP,
                    'TELLSTICK_DOWN', methods & self.TELLSTICK_DOWN,
                    'TELLSTICK_STOP', methods & self.TELLSTICK_STOP,
                )
                add_comp = '%s__%s' % (self.uuid, self.get_hadd_from_tdev(deviceid))
                #~ logger.debug('[%s] - Check node %s in %s', self.__class__.__name__, add_comp, self.nodeman.nodes)
                if add_comp not in self.nodeman.nodes:
                    #add_comp = key
                    hadd = HADD%(add_ctrl,self.get_hadd_from_tdev(deviceid))
                    compo_oid = '%s.device'%self.oid
                    if methods & self.TELLSTICK_DIM:
                        compo_oid = '%s.dimmer'%self.oid
                    if methods & self.TELLSTICK_UP and methods & self.TELLSTICK_UP:
                        compo_oid = '%s.shutter'%self.oid
                    compo = self.add_component(compo_oid, add_comp, options=self.options)
                    node = self.nodeman.create_node(add_comp, hadd, name=name)
                    node.create_options(compo_oid)
                    time.sleep(self.nodeman.slow_start)
                    logger.debug('[%s] - Discover new component %s / node %s', self.__class__.__name__, compo, node)
        logger.debug('[%s] - Found components %s after discover', self.__class__.__name__, self.components)
    self.tellstick_discover_new_devices = tellstick_discover_new_devices

    def tellstick_update_device_component(node_uuid, component_uuid):
        """We can't make a distinction between a switch, a remote controler, a door sensors or a light sensor.
        So we need to update it after discovering.
        """
        node = self.nodeman.find_node(node_uuid)
        #~ node = self.nodeman.find_node_by_hadd(node_hadd)
        logger.debug('[%s] - Found node %s with uid %s in %s', self.__class__.__name__, node, node_uuid, self.nodeman.nodes )
        add_ctrl, add_node = node.split_hadd()
        self.nodeman.mqtt_heartbeat.publish_heartbeat(int(add_ctrl), int(add_node), 'OFFLINE')
        del self.nodeman.nodes[node.uuid]
        self.components[node.uuid].stop()
        del self.components[node.uuid]
        compo = self.add_component(component_uuid, node.uuid, options=self.options)
        node = self.nodeman.create_node(node.uuid, node.hadd)
        node.update_bus_options(component_uuid)
        logger.debug('[%s] - Update component for node %s to %s', self.__class__.__name__, node, component_uuid )
    self.tellstick_update_device_component = tellstick_update_device_component

def extend_net( self ):
    pass
