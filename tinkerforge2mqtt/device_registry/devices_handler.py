import collections
import logging
import queue
import time

from ha_services.mqtt4homeassistant.converter import values2mqtt_payload
from ha_services.mqtt4homeassistant.data_classes import HaValue, HaValues
from ha_services.mqtt4homeassistant.mqtt import HaMqttPublisher
from tinkerforge.device_factory import get_device_class
from tinkerforge.ip_connection import Device, Error, IPConnection

import tinkerforge2mqtt
from tinkerforge2mqtt.device_map import map_registry
from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase
from tinkerforge2mqtt.mapping.device_value import DeviceValue
from tinkerforge2mqtt.mapping.value_map import HaValueInfo


logger = logging.getLogger(__name__)


class DevicesHandler:
    def __init__(
        self,
        ipcon: IPConnection,
        *,
        publisher: HaMqttPublisher | None = None,
        name_prefix: str = '',
        update_interval: int = 2,
    ):
        self.ipcon = ipcon
        self.publisher = publisher
        self.name_prefix = name_prefix
        self.update_interval = update_interval

        self._map_instances = {}
        self.ha_value_queue = queue.Queue()
        self.next_update = time.monotonic() + self.update_interval

    def ha_value_callback(self, *, device_mapper: DeviceMapBase, value, ha_value_info: HaValueInfo):
        logger.debug(f'HA value callback: {device_mapper}: {value=} {ha_value_info=}')
        device_value = DeviceValue(
            device_mapper=device_mapper,
            value=value,
            info=ha_value_info,
        )
        logger.info(f'{device_value=}')
        self.ha_value_queue.put(device_value)

        if time.monotonic() > self.next_update:
            self.push_values()
            self.next_update = time.monotonic() + self.update_interval

    def push_values(self):
        device_ha_values = collections.defaultdict(list)
        while not self.ha_value_queue.empty():
            device_value: DeviceValue = self.ha_value_queue.get()

            device_mapper: DeviceMapBase = device_value.device_mapper

            ha_value_info: HaValueInfo = device_value.info
            ha_value: HaValue = ha_value_info.get_ha_value(device_value.value)

            device_ha_values[device_mapper].append(ha_value)

        for device_mapper, values in device_ha_values.items():
            device: Device = device_mapper.device
            uid_string = device.uid_string
            device_name = device.DEVICE_DISPLAY_NAME
            device_name = f'{device_name} ({uid_string})'

            ha_values = HaValues(
                device_name=device_name,
                values=values,
            )
            logger.info(f'Send {len(values)} values for {device_name} to HomeAssistant')

            # Create Payload:
            ha_mqtt_payload = values2mqtt_payload(
                values=ha_values,
                name_prefix=self.name_prefix,
                device_extra_info={
                    'manufacturer': 'Tinkerforge',
                    'sw_version': device_mapper.get_sw_version(),
                },
                origin={
                    'name': 'tinkerforge2mqtt',
                    'sw_version': tinkerforge2mqtt.__version__,
                    'support_url': 'https://pypi.org/project/tinkerforge2mqtt/',
                },
            )

            # Send vial MQTT to HomeAssistant:
            self.publisher.publish2homeassistant(ha_mqtt_payload=ha_mqtt_payload)

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
            print('Disconnected!')
            return

        if map_instance := self._map_instances.get(uid):
            # Already initialized device -> poll values
            try:
                map_instance.poll()
            except Error as err:
                logger.exception(f'Error in poll: {err}')
        else:
            # Initialize new device

            DeviceClass = get_device_class(device_identifier)
            print('_' * 80)
            print(f'{DeviceClass.DEVICE_DISPLAY_NAME} ({DeviceClass.__name__})')

            MapClass = map_registry.get_map_class(device_identifier)
            if not MapClass:
                logger.error(f'No mapper found for {DeviceClass.__name__} ({device_identifier=})')
                return

            device: Device = DeviceClass(uid=uid, ipcon=self.ipcon)
            map_instance = MapClass(device=device, ha_value_callback=self.ha_value_callback)
            map_instance.register_callbacks()
            self._map_instances[uid] = map_instance
            print(f'{map_instance=}')
