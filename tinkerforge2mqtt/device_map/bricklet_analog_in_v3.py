import logging

from ha_services.mqtt4homeassistant.components.sensor import Sensor
from tinkerforge.bricklet_analog_in_v3 import BrickletAnalogInV3

from tinkerforge2mqtt.device_map import register_map_class
from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase, print_exception_decorator


logger = logging.getLogger(__name__)


INTERVAL_DURATION = 0.0175  # 17,5µs
OVERSAMPLING_MAP = {
    0: 32,  # 32x17,5µs = 0.56ms
    1: 64,
    2: 128,
    3: 256,
    4: 512,
    5: 1024,
    6: 2048,
    7: 4096,  # 4096x17,5µs = 71.68ms **the default**
    8: 8192,
    9: 16384,  # 16384x17,5µs = 286.72ms
}


def human_readable_oversampling(oversampling: int):
    """
    >>> human_readable_oversampling(0)
    '32x (0.56ms)'
    >>> human_readable_oversampling(7)
    '4096x (71.68ms)'
    >>> human_readable_oversampling(9)
    '16384x (286.72ms)'
    """
    assert oversampling in OVERSAMPLING_MAP, f'Invalid: {oversampling=}'
    factor = OVERSAMPLING_MAP[oversampling]
    duration = factor * INTERVAL_DURATION
    return f'{factor}x ({duration:.2f}ms)'


@register_map_class()
class BrickletAnalogInV3Mapper(DeviceMapBase):
    # https://www.tinkerforge.com/de/doc/Software/Bricklets/AnalogInV3_Bricklet_Python.html

    device_identifier = BrickletAnalogInV3.DEVICE_IDENTIFIER

    def __init__(self, *, device: BrickletAnalogInV3, **kwargs):
        self.device: BrickletAnalogInV3 = device
        super().__init__(device=device, **kwargs)

    @print_exception_decorator
    def setup_sensors(self):
        super().setup_sensors()

        self.voltage = Sensor(
            device=self.mqtt_device,
            name='Voltage',
            uid='voltage',
            device_class='voltage',
            state_class='measurement',
            unit_of_measurement='V',
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

    @print_exception_decorator
    def callback_voltage(self, value):
        logger.info(f'Voltage callback: {value}mV (UID: {self.device.uid_string})')
        voltage = value / 1000.0
        self.voltage.set_state(voltage)
        self.voltage.publish(self.mqtt_client)

        # TODO: Poll the oversampling value and expose it as MQTT "select"
        #       After: https://github.com/jedie/ha-services/issues/70
        # oversampling = self.device.get_oversampling()
        # print(f'{oversampling=}', human_readable_oversampling(oversampling))
