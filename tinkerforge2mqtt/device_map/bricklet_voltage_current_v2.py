import logging

from ha_services.mqtt4homeassistant.components.sensor import Sensor
from tinkerforge.bricklet_voltage_current_v2 import BrickletVoltageCurrentV2

from tinkerforge2mqtt.device_map import register_map_class
from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase, print_exception_decorator


logger = logging.getLogger(__name__)


@register_map_class()
class BrickletVoltageCurrentV2Mapper(DeviceMapBase):
    # https://www.tinkerforge.com/de/doc/Software/Bricklets/VoltageCurrentV2_Bricklet_Python.html

    device_identifier = BrickletVoltageCurrentV2.DEVICE_IDENTIFIER

    def __init__(self, *, device: BrickletVoltageCurrentV2, **kwargs):
        self.device: BrickletVoltageCurrentV2 = device
        super().__init__(device=device, **kwargs)

    @print_exception_decorator
    def setup_sensors(self):
        super().setup_sensors()

        self.current = Sensor(
            device=self.mqtt_device,
            name='Current',
            uid='current',
            device_class='current',
            state_class='measurement',
            unit_of_measurement='A',
            suggested_display_precision=3,
        )
        self.voltage = Sensor(
            device=self.mqtt_device,
            name='Voltage',
            uid='voltage',
            device_class='voltage',
            state_class='measurement',
            unit_of_measurement='V',
            suggested_display_precision=3,
        )
        self.power = Sensor(
            device=self.mqtt_device,
            name='Power',
            uid='power',
            device_class='power',
            state_class='measurement',
            unit_of_measurement='W',
            suggested_display_precision=3,
        )

    @print_exception_decorator
    def setup_callbacks(self):
        super().setup_callbacks()
        self.device.set_voltage_callback_configuration(
            period=self.user_settings.callback_period * 1000,
            value_has_to_change=False,
            option=self.device.THRESHOLD_OPTION_OFF,
            min=0,
            max=0,
        )
        self.device.register_callback(self.device.CALLBACK_VOLTAGE, self.callback_voltage)

        self.device.set_current_callback_configuration(
            period=self.user_settings.callback_period * 1000,
            value_has_to_change=False,
            option=self.device.THRESHOLD_OPTION_OFF,
            min=0,
            max=0,
        )
        self.device.register_callback(self.device.CALLBACK_CURRENT, self.callback_current)

        self.device.set_power_callback_configuration(
            period=self.user_settings.callback_period * 1000,
            value_has_to_change=False,
            option=self.device.THRESHOLD_OPTION_OFF,
            min=0,
            max=0,
        )
        self.device.register_callback(self.device.CALLBACK_POWER, self.callback_power)

    @print_exception_decorator
    def callback_voltage(self, value):
        logger.info(f'Voltage callback: {value}mV (UID: {self.device.uid_string})')
        voltage = value / 1000.0
        self.voltage.set_state(voltage)
        self.voltage.publish_config_and_state(self.mqtt_client)

    @print_exception_decorator
    def callback_current(self, value):
        logger.info(f'Current callback: {value}mA (UID: {self.device.uid_string})')
        current = value / 1000.0
        self.current.set_state(current)
        self.current.publish_config_and_state(self.mqtt_client)

    @print_exception_decorator
    def callback_power(self, value):
        logger.info(f'Current callback: {value}mW (UID: {self.device.uid_string})')
        power = value / 1000.0
        self.power.set_state(power)
        self.power.publish_config_and_state(self.mqtt_client)
