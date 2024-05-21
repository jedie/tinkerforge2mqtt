import abc
import logging

from ha_services.mqtt4homeassistant.components.sensor import Sensor
from ha_services.mqtt4homeassistant.device import MainMqttDevice, MqttDevice
from paho.mqtt.client import Client
from rich import print  # noqa
from tinkerforge.ip_connection import Device

from tinkerforge2mqtt.device_map_utils.generics import iter_interest_functions
from tinkerforge2mqtt.device_map_utils.led_config import BrickletLedConfigSelect
from tinkerforge2mqtt.device_map_utils.utils import print_exception_decorator
from tinkerforge2mqtt.user_settings import UserSettings


logger = logging.getLogger(__name__)


class DeviceMapBase(abc.ABC):
    device_identifier: int

    @abc.abstractmethod
    def __init__(
        self,
        *,
        main_mqtt_device: MainMqttDevice,
        device: Device,
        mqtt_client: Client,
        user_settings: UserSettings,
    ):
        self.main_mqtt_device = main_mqtt_device
        self.device = device
        self.mqtt_client = mqtt_client
        self.user_settings = user_settings

        self.mqtt_device = MqttDevice(
            main_device=main_mqtt_device,
            name=f'{device.DEVICE_DISPLAY_NAME} ({device.uid_string})',
            uid=device.uid_string,
            manufacturer='Tinkerforge',
            model=device.DEVICE_DISPLAY_NAME,
            sw_version=self.get_sw_version(),
        )

        self.setup_sensors()
        self.setup_callbacks()
        self.poll()

    @abc.abstractmethod
    def setup_sensors(self):
        if hasattr(self.device, 'get_chip_temperature'):
            self.chip_temperature_sensor = Sensor(
                device=self.mqtt_device,
                name='Chip Temperature',
                uid='chip_temperature',
                device_class='temperature',
                state_class='measurement',
                unit_of_measurement='°C',
                suggested_display_precision=0,
            )
            logger.info(f'Sensor: {self.chip_temperature_sensor}')

        if hasattr(self.device, 'get_status_led_config'):
            self.led_config_sensor = BrickletLedConfigSelect(device=self.device, mqtt_device=self.mqtt_device)
            logger.info(f'Sensor: {self.led_config_sensor}')

    @abc.abstractmethod
    def setup_callbacks(self):
        pass

    def iter_known_functions(self, device: Device):
        assert (
            device.DEVICE_IDENTIFIER == self.device_identifier
        ), f'Wrong device: {device} is not {self.device_identifier}'

        yield from iter_interest_functions(device)

    @print_exception_decorator
    def poll(self):
        logger.info(f'Polling {self.device.DEVICE_DISPLAY_NAME} ({self.device.uid_string})')

        if get_chip_temperature := getattr(self.device, 'get_chip_temperature', None):
            value = get_chip_temperature()
            logger.debug(f'{self.device.DEVICE_DISPLAY_NAME} chip temperature: {value}°C')
            self.chip_temperature_sensor.set_state(state=value)
            self.chip_temperature_sensor.publish(self.mqtt_client)
            logger.info(f'Chip temperature: {value}°C: {self.chip_temperature_sensor}')

        if hasattr(self, 'led_config_sensor'):
            self.led_config_sensor.poll(self.mqtt_client)

        self.main_mqtt_device.poll_and_publish(self.mqtt_client)

    def get_sw_version(self) -> str:
        api_version = self.device.get_api_version()
        sw_version = '.'.join(str(number) for number in api_version)
        return sw_version

    def __str__(self):
        return f'{self.__class__.__name__} (UID: {self.device.uid_string})'

    def __repr__(self):
        return f'<{self}>'
