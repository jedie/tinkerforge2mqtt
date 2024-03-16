import logging

from tinkerforge.brick_hat_zero import BrickHATZero

from tinkerforge2mqtt.device_map import register_map_class
from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase, print_exception_decorator
from tinkerforge2mqtt.mapping.value_map import ValueMap


logger = logging.getLogger(__name__)


@register_map_class()
class BrickHATZeroMapper(DeviceMapBase):
    # https://www.tinkerforge.com/de/doc/Software/Bricks/HATZero_Brick_Python.html

    device_identifier = BrickHATZero.DEVICE_IDENTIFIER

    def __init__(self, device: BrickHATZero, ha_value_callback):
        self.device = device
        self.ha_value_callback = ha_value_callback

    def register_callbacks(self):
        self.device.set_usb_voltage_callback_configuration(
            period=1000,  # 1000ms == 1s
            value_has_to_change=False,
            option='x',  # Threshold is turned off
            min=0,
            max=999,
        )
        self.device.register_callback(self.device.CALLBACK_USB_VOLTAGE, self.callback_usb_voltage)

    @print_exception_decorator
    def callback_usb_voltage(self, value):
        logger.debug(f'USB Voltage: {value / 1000}V (UID: {self.device.uid_string})')
        self.ha_value_callback(
            device_mapper=self,
            value=value / 1000,
            ha_value_info=ValueMap.USB_VOLTAGE,
        )
