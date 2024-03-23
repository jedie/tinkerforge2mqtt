import abc
import logging
import threading
from functools import wraps

from ha_mqtt_discoverable import DeviceInfo, Settings
from ha_mqtt_discoverable.sensors import Sensor, SensorInfo
from rich import print  # noqa
from rich.console import Console
from tinkerforge.ip_connection import Device

from tinkerforge2mqtt.device_map_utils.generics import iter_interest_functions
from tinkerforge2mqtt.user_settings import UserSettings


logger = logging.getLogger(__name__)


def print_exception_decorator(func):

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            console = Console()
            console.print_exception(show_locals=True)
            raise SystemExit from err

    return func_wrapper


class DeviceMapBase(abc.ABC):
    device_identifier: int

    @abc.abstractmethod
    def __init__(
        self,
        *,
        device: Device,
        mqtt_settings: Settings.MQTT,
        user_settings: UserSettings,
    ):
        self.mqtt_settings = mqtt_settings
        self.user_settings = user_settings
        self.device_info = DeviceInfo(
            name=f'TEST {device.DEVICE_DISPLAY_NAME} ({device.uid_string})',
            identifiers=f'{self.user_settings.mqtt.unique_id_prefix}-{device.uid_string}',
            manufacturer='Tinkerforge',
            sw_version=self.get_sw_version(),
        )

        self._device_lock = threading.Lock()

        self.setup_sensors()
        self.setup_callbacks()
        self.poll()

    @abc.abstractmethod
    def setup_sensors(self):
        if hasattr(self.device, 'get_chip_temperature'):
            chip_temperature_sensor_info = SensorInfo(
                name='Chip Temperature',
                unit_of_measurement='°C',
                state_class='measurement',
                device_class='temperature',
                unique_id=f'{self.user_settings.mqtt.unique_id_prefix}-chip_temperature_{self.device.uid_string}',
                device=self.device_info,
            )
            logger.debug(f'Creating sensor info: {chip_temperature_sensor_info}')
            chip_temperature_sensor_settings = Settings(mqtt=self.mqtt_settings, entity=chip_temperature_sensor_info)
            self.chip_temperature_sensor = Sensor(settings=chip_temperature_sensor_settings)
            logger.info(f'Sensor: {self.chip_temperature_sensor}')

        if hasattr(self.device, 'get_status_led_config'):
            led_config_sensor_info = SensorInfo(
                name='LED Config',
                device_class='enum',
                unique_id=f'{self.user_settings.mqtt.unique_id_prefix}-led_config_{self.device.uid_string}',
                device=self.device_info,
            )
            logger.debug(f'Creating sensor info: {led_config_sensor_info}')
            led_config_sensor_settings = Settings(mqtt=self.mqtt_settings, entity=led_config_sensor_info)
            self.led_config_sensor = Sensor(settings=led_config_sensor_settings)
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
            logger.warning(f'Chip temperature: {value}°C: {self.chip_temperature_sensor}')

        if get_status_led_config := getattr(self.device, 'get_status_led_config', None):
            value = get_status_led_config()
            logger.warning(f'{self.device.DEVICE_DISPLAY_NAME} status LED config: {value}')
            self.led_config_sensor.set_state(state=value)

    def get_sw_version(self) -> str:
        api_version = self.device.get_api_version()
        sw_version = '.'.join(str(number) for number in api_version)
        return sw_version

    def __str__(self):
        return f'{self.__class__.__name__} (UID: {self.device.uid_string})'

    def __repr__(self):
        return f'<{self}>'
