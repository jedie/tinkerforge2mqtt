import logging

from tinkerforge.bricklet_industrial_dual_relay import BrickletIndustrialDualRelay
from tinkerforge.bricklet_motion_detector_v2 import BrickletMotionDetectorV2
from tinkerforge.bricklet_temperature_v2 import BrickletTemperatureV2

from tinkerforge2mqtt.device_map import register_map_class
from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase, print_exception_decorator
from tinkerforge2mqtt.mapping.value_map import ValueMap


logger = logging.getLogger(__name__)


@register_map_class()
class BrickletTemperatureV2Mapper(DeviceMapBase):
    # https://www.tinkerforge.com/de/doc/Software/Bricks/HATZero_Brick_Python.html

    device_identifier = BrickletTemperatureV2.DEVICE_IDENTIFIER

    def __init__(self, device: BrickletTemperatureV2, ha_value_callback):
        self.device = device
        self.ha_value_callback = ha_value_callback

    def register_callbacks(self):
        self.device.set_temperature_callback_configuration(
            period=1000,  # 1000ms == 1s
            value_has_to_change=False,
            option=BrickletTemperatureV2.THRESHOLD_OPTION_OFF,
            min=-999,
            max=999,
        )
        self.device.register_callback(self.device.CALLBACK_TEMPERATURE, self.callback_temperature)

    @print_exception_decorator
    def callback_temperature(self, value):
        logger.debug(f'Temperature: {value / 100}°C (UID: {self.device.uid_string})')
        self.ha_value_callback(
            device_mapper=self,
            value=value / 100,
            ha_value_info=ValueMap.TEMPERATURE,
        )


@register_map_class()
class BrickletIndustrialDualRelayMapper(DeviceMapBase):
    # https://www.tinkerforge.com/de/doc/Software/Bricklets/IndustrialDualRelay_Bricklet_Python.html

    device_identifier = BrickletIndustrialDualRelay.DEVICE_IDENTIFIER

    def __init__(self, device: BrickletIndustrialDualRelay, ha_value_callback):
        self.device = device
        self.ha_value_callback = ha_value_callback

    def register_callbacks(self):
        self.device.register_callback(self.device.CALLBACK_MONOFLOP_DONE, self.callback_monoflop_done)

    @print_exception_decorator
    def callback_monoflop_done(self, value):
        logger.debug(f'Temperature: {value / 100}°C (UID: {self.device.uid_string})')
        self.ha_value_callback(
            device_mapper=self,
            value=value / 100,
            ha_value_info=ValueMap.TEMPERATURE,
        )


@register_map_class()
class BrickletMotionDetectorV2Mapper(DeviceMapBase):
    # https://www.tinkerforge.com/de/doc/Software/Bricklets/MotionDetectorV2_Bricklet_Python.html

    device_identifier = BrickletMotionDetectorV2.DEVICE_IDENTIFIER

    def __init__(self, device: BrickletMotionDetectorV2, ha_value_callback):
        self.device = device
        self.ha_value_callback = ha_value_callback

    @print_exception_decorator
    def poll(self):
        super().poll()
        sensitivity = self.device.get_sensitivity()
        self.ha_value_callback(
            device_mapper=self,
            value=sensitivity,
            ha_value_info=ValueMap.PIR_SENSOR_SENSITIVITY,
        )

    def register_callbacks(self):
        self.device.register_callback(self.device.CALLBACK_MOTION_DETECTED, self.callback_motion_detected)
        self.device.register_callback(self.device.CALLBACK_DETECTION_CYCLE_ENDED, self.callback_detection_cycle_ended)

    @print_exception_decorator
    def callback_motion_detected(self, value):
        logger.debug(f'Motion detected: {value=} (UID: {self.device.uid_string})')
        self.ha_value_callback(
            device_mapper=self,
            value=value,
            ha_value_info=ValueMap.MOTION_DETECTED,
        )

    @print_exception_decorator
    def callback_detection_cycle_ended(self, value):
        logger.debug(f'Detection Cycle Ended: {value} (UID: {self.device.uid_string})')
        self.ha_value_callback(
            device_mapper=self,
            value=value,
            ha_value_info=ValueMap.DETECTION_CYCLE_ENDED,
        )
