# -*- coding: utf-8 -*-
"""The Raspberry tellstick bus
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

    def __init__(self, **kwargs):
        """
        :param int bus_id: the SMBus id (see Raspberry Pi documentation)
        :param kwargs: parameters transmitted to :py:class:`smbus.SMBus` initializer
        """
        JNTBus.__init__(self, **kwargs)
        self._tellstick_lock = threading.Lock()
        self.load_extensions(OID)

        # Commands
        self.TELLSTICK_TURNON = 1
        self.TELLSTICK_TURNOFF = 2
        self.TELLSTICK_BELL = 4
        self.TELLSTICK_TOGGLE = 8
        self.TELLSTICK_DIM = 16
        self.TELLSTICK_LEARN = 32
        self.TELLSTICK_EXECUTE = 64
        self.TELLSTICK_UP = 128
        self.TELLSTICK_DOWN = 256
        self.TELLSTICK_STOP = 512
        self.ALL_METHODS = self.TELLSTICK_TURNON | self.TELLSTICK_TURNOFF | self.TELLSTICK_BELL | \
                           self.TELLSTICK_DIM | self.TELLSTICK_UP | self.TELLSTICK_DOWN | \
                           self.TELLSTICK_STOP

        #Sensors
        self.TELLSTICK_TEMPERATURE = 1
        self.TELLSTICK_HUMIDITY = 2
        self.TELLSTICK_RAINRATE = 4
        self.TELLSTICK_RAINTOTAL = 8
        self.TELLSTICK_WINDDIRECTION = 16
        self.TELLSTICK_WINDAVERAGE = 32
        self.TELLSTICK_WINDGUST = 64

        # Error codes
        self.TELLSTICK_SUCCESS = 0
        self.TELLSTICK_ERROR_NOT_FOUND = -1
        self.TELLSTICK_ERROR_PERMISSION_DENIED = -2
        self.TELLSTICK_ERROR_DEVICE_NOT_FOUND = -3
        self.TELLSTICK_ERROR_METHOD_NOT_SUPPORTED = -4
        self.TELLSTICK_ERROR_COMMUNICATION = -5
        self.TELLSTICK_ERROR_CONNECTING_SERVICE = -6
        self.TELLSTICK_ERROR_UNKNOWN_RESPONSE = -7
        self.TELLSTICK_ERROR_SYNTAX = -8
        self.TELLSTICK_ERROR_BROKEN_PIPE = -9
        self.TELLSTICK_ERROR_COMMUNICATING_SERVICE = -10
        self.TELLSTICK_ERROR_CONFIG_SYNTAX = -11
        self.TELLSTICK_ERROR_UNKNOWN = -99

        # Controller typedef
        self.TELLSTICK_CONTROLLER_TELLSTICK = 1
        self.TELLSTICK_CONTROLLER_TELLSTICK_DUO = 2
        self.TELLSTICK_CONTROLLER_TELLSTICK_NET = 3

        # Device changes
        self.TELLSTICK_DEVICE_ADDED = 1
        self.TELLSTICK_DEVICE_CHANGED = 2
        self.TELLSTICK_DEVICE_REMOVED = 3
        self.TELLSTICK_DEVICE_STATE_CHANGED = 4

        # Change types
        self.TELLSTICK_CHANGE_NAME = 1
        self.TELLSTICK_CHANGE_PROTOCOL = 2
        self.TELLSTICK_CHANGE_MODEL = 3
        self.TELLSTICK_CHANGE_METHOD = 4
        self.TELLSTICK_CHANGE_AVAILABLE = 5
        self.TELLSTICK_CHANGE_FIRMWARE = 6

        self._lock_delay = 0.5

        self.export_attrs('tellstick_acquire', self.tellstick_acquire)
        self.export_attrs('tellstick_release', self.tellstick_release)
        self.export_attrs('tellstick_locked', self.tellstick_locked)
        self.export_attrs('tellstick_turnon', self.tellstick_turnon)
        self.export_attrs('tellstick_turnoff', self.tellstick_turnoff)
        self.export_attrs('tellstick_dim', self.tellstick_dim)
        self.export_attrs('tellstick_bell', self.tellstick_bell)
        self.export_attrs('tellstick_execute', self.tellstick_execute)
        self.export_attrs('tellstick_up', self.tellstick_up)
        self.export_attrs('tellstick_down', self.tellstick_down)
        self.export_attrs('tellstick_stop', self.tellstick_stop)

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

    def get_hadd_from_tdev(tdev):
        """
        """
        return tdev+1
    self.get_hadd_from_tdev = get_hadd_from_tdev

    def get_tdev_from_hadd(hadd):
        """
        """
        return hadd-1
    self.get_tdev_from_hadd = get_tdev_from_hadd

    def event_device_change_callback(device_id, change_event, change_type, callback_id, context):
        """
        """
        logger.debug("[%s] - Receive change %s callback for %s", self.__class__.__name__,change_event , device_id)
        return True
    self.event_device_change_callback = event_device_change_callback
    self.event_change_device = None
    self.export_attrs('event_change_device', self.event_change_device)

    def event_device_callback(device_id, method, value, callback_id):
        """
        """
        logger.debug("[%s] - Receive callback from %s", self.__class__.__name__, device_id)
        return True
    self.event_device_callback = event_device_callback
    self.event_device = None
    self.export_attrs('event_device', self.event_device)

    self._telldusduo_start = self.start
    def start(mqttc, trigger_thread_reload_cb=None):
        """Start the bus"""
        logger.debug("[%s] - Start the bus %s", self.__class__.__name__, self.oid )
        try:
            self.event_change_device = telldus.tdRegisterDeviceChangeEvent(self.event_device_change_callback)
            self.export_attrs('event_change_device', self.event_change_device)
            self.event_device = telldus.tdRegisterDeviceEvent(self.event_device_callback)
            self.export_attrs('event_device', self.event_device)
        except Exception:
            logger.exception('[%s] - Exception when starting bus %s', self.__class__.__name__, self.oid)
        return self._telldusduo_start(mqttc, trigger_thread_reload_cb=trigger_thread_reload_cb)
    self.start = start

    self._telldusduo_stop = self.stop
    def stop():
        """stop the bus"""
        logger.debug("[%s] - Stop the bus %s", self.__class__.__name__, self.oid )
        try:
            if self.event_change_device is not None:
                telldus.tdUnregisterCallback(self.event_change_device)
                self.event_change_device = None
                self.export_attrs('event_change_device', self.event_change_device)
            if self.event_device is not None:
                telldus.tdUnregisterCallback(self.event_device)
                self.event_device = None
                self.export_attrs('event_device', self.event_device)
            telldus.tdClose()
        except Exception:
            logger.exception('[%s] - Exception when stopping bus %s', self.__class__.__name__, self.oid)
        return self._telldusduo_stop()
    self.stop = stop

    self._telldusduo_del__ = self.__del__
    def __del__():
        """stop the bus"""
        logger.debug("[%s] - __del__ the bus %s", self.__class__.__name__, self.oid )
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
        """Dim a telldus device. Level from 0 to 255."""
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
        """execute a telldus device. Level from 0 to 255."""
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

    def tellstick_up(tdev, level):
        """up a telldus device."""
        self.tellstick_acquire()
        try:
            methods = telldus.tdMethods(tdev, self.ALL_METHODS)
            if methods & self.TELLSTICK_UP:
                telldus.tdUp(tdev)
                time.sleep(self._lock_delay)
        except Exception:
            logger.exception('[%s] - Exception when tellstick_up', self.__class__.__name__)
        finally:
            self.tellstick_release()
    self.tellstick_up = tellstick_up

    def tellstick_down(tdev, level):
        """down a telldus device. Level from 0 to 255."""
        self.tellstick_acquire()
        try:
            methods = telldus.tdMethods(tdev, self.ALL_METHODS)
            if methods & self.TELLSTICK_DOWN:
                telldus.tdDown(tdev)
                time.sleep(self._lock_delay)
        except Exception:
            logger.exception('[%s] - Exception when tellstick_down', self.__class__.__name__)
        finally:
            self.tellstick_release()
    self.tellstick_down = tellstick_down

    def tellstick_stop(tdev, level):
        """stop a telldus device. Level from 0 to 255."""
        self.tellstick_acquire()
        try:
            methods = telldus.tdMethods(tdev, self.ALL_METHODS)
            if methods & self.TELLSTICK_STOP:
                telldus.tdStop(tdev)
                time.sleep(self._lock_delay)
        except Exception:
            logger.exception('[%s] - Exception when tellstick_stop', self.__class__.__name__)
        finally:
            self.tellstick_release()
    self.tellstick_stop = tellstick_stop

    def tellstick_bell(tdev, level):
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

    def tellstick_learn(tdev, level):
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

    def tellstick_update_device_component(node_hadd, component_uuid):
        """We can't make a distinction between a switch, a remote controler, a door sensors or a light sensor.
        So we need to update it after discovering.
        """
        node = self.nodeman.find_node_by_hadd(node_hadd)
        logger.debug('[%s] - Found node %s with uid %s in %s', self.__class__.__name__, node, node_hadd, self.nodeman.nodes )
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
