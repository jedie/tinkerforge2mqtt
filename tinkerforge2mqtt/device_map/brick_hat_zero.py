import logging

from ha_services.mqtt4homeassistant.components.sensor import Sensor
from tinkerforge.brick_hat_zero import BrickHATZero

from tinkerforge2mqtt.device_map import register_map_class
from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase, print_exception_decorator


logger = logging.getLogger(__name__)


@register_map_class()
class BrickHATZeroMapper(DeviceMapBase):
    # https://www.tinkerforge.com/de/doc/Software/Bricks/HATZero_Brick_Python.html

    device_identifier = BrickHATZero.DEVICE_IDENTIFIER

    def __init__(self, *, device: BrickHATZero, **kwargs):
        self.device: BrickHATZero = device
        super().__init__(device=device, **kwargs)

    @print_exception_decorator
    def setup_sensors(self):
        super().setup_sensors()
        self.usb_voltage_sensor = Sensor(
            device=self.mqtt_device,
            name='USB Voltage',
            uid='voltage',
            device_class='voltage',
            state_class='measurement',
            unit_of_measurement='V',
            suggested_display_precision=3,
        )
        logger.info(f'Sensor: {self.usb_voltage_sensor}')

    @print_exception_decorator
    def setup_callbacks(self):
        super().setup_callbacks()
        self.device.set_usb_voltage_callback_configuration(
            period=self.user_settings.callback_period * 1000,
            value_has_to_change=False,
            option='x',  # Threshold is turned off
            min=0,
            max=999,
        )
        self.device.register_callback(BrickHATZero.CALLBACK_USB_VOLTAGE, self.callback_usb_voltage)
        self.callback_usb_voltage(value=self.device.get_usb_voltage())

    @print_exception_decorator
    def callback_usb_voltage(self, value):
        logger.debug(f'USB Voltage: {value / 1000}V (UID: {self.device.uid_string})')
        self.usb_voltage_sensor.set_state(state=value / 1000)
        self.usb_voltage_sensor.publish_config_and_state(self.mqtt_client)
