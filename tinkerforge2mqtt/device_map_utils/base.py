import abc
import logging
from functools import wraps

from rich import print  # noqa
from rich.console import Console
from tinkerforge.ip_connection import Device

from tinkerforge2mqtt.device_map_utils.generics import iter_interest_functions
from tinkerforge2mqtt.mapping.value_map import ValueMap


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
    def __init__(self, device: Device, ha_value_callback):
        self.device = device
        self.ha_value_callback = ha_value_callback

    def iter_known_functions(self, device: Device):
        assert (
            device.DEVICE_IDENTIFIER == self.device_identifier
        ), f'Wrong device: {device} is not {self.device_identifier}'

        yield from iter_interest_functions(device)

    @print_exception_decorator
    def poll(self):
        value = self.device.get_chip_temperature()
        logger.debug(f'{self.device.DEVICE_DISPLAY_NAME} chip temperature: {value}°C')
        self.ha_value_callback(
            device_mapper=self,
            value=value,
            ha_value_info=ValueMap.CHIP_TEMPERATURE,
        )

        if get_status_led_config := getattr(self.device, 'get_status_led_config', None):
            value = get_status_led_config()
            logger.debug(f'{self.device.DEVICE_DISPLAY_NAME} status LED config: {value}')
            self.ha_value_callback(
                device_mapper=self,
                value=value,
                ha_value_info=ValueMap.STATUS_LED_CONFIG,
            )

    @abc.abstractmethod
    def register_callbacks(self):
        pass

    def get_sw_version(self) -> str:
        api_version = self.device.get_api_version()
        sw_version = '.'.join(str(number) for number in api_version)
        return sw_version

    def __str__(self):
        return f'{self.__class__.__name__} (UID: {self.device.uid_string})'

    def __repr__(self):
        return f'<{self}>'
