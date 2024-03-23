import logging
import threading

from ha_mqtt_discoverable import Settings
from tinkerforge.device_factory import get_device_class
from tinkerforge.ip_connection import Device, IPConnection

from tinkerforge2mqtt.device_map import map_registry
from tinkerforge2mqtt.user_settings import UserSettings


logger = logging.getLogger(__name__)


class DevicesHandler:
    def __init__(
        self,
        ipcon: IPConnection,
        *,
        user_settings: UserSettings,
    ):
        self.ipcon = ipcon
        self.user_settings = user_settings

        self.mqtt_settings = Settings.MQTT(
            host=user_settings.mqtt.host,
            port=user_settings.mqtt.port,
            username=user_settings.mqtt.user_name,
            password=user_settings.mqtt.password,
            client_name='tinkerforge2mqtt',
            discovery_prefix='homeassistant',
            state_prefix='homeassistant',
        )

        self.map_instances = {}
        self._enumerate_handler_lock = threading.Lock()

    def enumerate_handler(
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

        with self._enumerate_handler_lock:
            if map_instance := self.map_instances.get(uid):
                print('Already initialized:', map_instance)
            else:
                print('New device:', locals())
                import traceback
                traceback.print_stack()
                TinkerforgeDeviceClass = get_device_class(device_identifier)
                print('_' * 80)
                name = f'{TinkerforgeDeviceClass.DEVICE_DISPLAY_NAME} ({TinkerforgeDeviceClass.__name__})'
                print(name)

                MapClass = map_registry.get_map_class(device_identifier)
                if not MapClass:
                    logger.error(f'No mapper found for {TinkerforgeDeviceClass.__name__} ({device_identifier=})')
                    return

                device: Device = TinkerforgeDeviceClass(uid=uid, ipcon=self.ipcon)

                map_instance = MapClass(
                    device=device,
                    mqtt_settings=self.mqtt_settings,
                    user_settings=self.user_settings,
                )
                self.map_instances[uid] = map_instance

        map_instance.poll()

    def connected_handler(self, *args, **kwargs):
        print('Connected!', args, kwargs, self.ipcon.devices)

    def disconnected_handler(self, *args, **kwargs):
        print('Disconnected!', args, kwargs)
