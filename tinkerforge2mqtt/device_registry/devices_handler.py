import logging

from ha_services.mqtt4homeassistant.device import MainMqttDevice
from paho.mqtt.client import Client
from tinkerforge.device_factory import get_device_class
from tinkerforge.ip_connection import Device, IPConnection

import tinkerforge2mqtt
from tinkerforge2mqtt.device_map import map_registry
from tinkerforge2mqtt.user_settings import UserSettings


logger = logging.getLogger(__name__)


class DevicesHandler:
    def __init__(
        self,
        ipcon: IPConnection,
        *,
        mqtt_client: Client,
        user_settings: UserSettings,
    ):
        self.ipcon = ipcon
        self.mqtt_client = mqtt_client
        self.user_settings = user_settings

        self.main_mqtt_device = MainMqttDevice(
            name='tinkerforge2mqtt',
            uid='tinkerforge2mqtt',
            manufacturer='tinkerforge2mqtt',
            sw_version=tinkerforge2mqtt.__version__,
        )

        self.map_instances = {}

    def __call__(
        self,
        uid,
        connected_uid,
        position,
        hardware_version,
        firmware_version,
        device_identifier,
        enumeration_type,
    ):
        if enumeration_type == IPConnection.ENUMERATION_TYPE_DISCONNECTED:
            logger.warning(f'Disconnected: {uid=}')
            return

        if map_instance := self.map_instances.get(uid):
            logger.debug(f'Already initialized: {uid=} {device_identifier=} {map_instance=}')
        else:
            logger.info(f'New device: {uid=} {device_identifier=}')

            TinkerforgeDeviceClass = get_device_class(device_identifier)
            name = f'{TinkerforgeDeviceClass.DEVICE_DISPLAY_NAME} ({TinkerforgeDeviceClass.__name__})'
            logger.info(name)

            MapClass = map_registry.get_map_class(device_identifier)
            if not MapClass:
                logger.error(f'No mapper found for {TinkerforgeDeviceClass.__name__} ({device_identifier=})')
                return

            device: Device = TinkerforgeDeviceClass(
                uid=uid,
                ipcon=self.ipcon,
            )

            map_instance = MapClass(
                main_mqtt_device=self.main_mqtt_device,
                device=device,
                mqtt_client=self.mqtt_client,
                user_settings=self.user_settings,
            )
            self.map_instances[uid] = map_instance

        map_instance.poll()

    def connected_handler(self, *args, **kwargs):
        print('Connected!', args, kwargs, self.ipcon.devices)

    def disconnected_handler(self, *args, **kwargs):
        print('Disconnected!', args, kwargs)
