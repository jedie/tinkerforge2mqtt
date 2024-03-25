import logging

from ha_services.mqtt4homeassistant.components.binary_sensor import BinarySensor
from tinkerforge.bricklet_motion_detector_v2 import BrickletMotionDetectorV2

from tinkerforge2mqtt.device_map import register_map_class
from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase, print_exception_decorator


logger = logging.getLogger(__name__)


@register_map_class()
class BrickletMotionDetectorV2Mapper(DeviceMapBase):
    # https://www.tinkerforge.com/de/doc/Software/Bricklets/MotionDetectorV2_Bricklet_Python.html

    device_identifier = BrickletMotionDetectorV2.DEVICE_IDENTIFIER

    def __init__(self, *, device: BrickletMotionDetectorV2, **kwargs):
        self.device: BrickletMotionDetectorV2 = device
        super().__init__(device=device, **kwargs)

    @print_exception_decorator
    def setup_sensors(self):
        super().setup_sensors()

        self.motion_detected = BinarySensor(
            device=self.mqtt_device,
            name='Motion Detected',
            uid='motion_detected',
            device_class='motion',
        )
        logger.info(f'Creating: {self.motion_detected}')

    @print_exception_decorator
    def setup_callbacks(self):
        super().setup_callbacks()
        self.device.register_callback(self.device.CALLBACK_MOTION_DETECTED, self.callback_motion_detected)
        self.device.register_callback(self.device.CALLBACK_DETECTION_CYCLE_ENDED, self.callback_detection_cycle_ended)

    @print_exception_decorator
    def callback_motion_detected(self):
        logger.debug(f'Motion detected (UID: {self.device.uid_string})')
        self.motion_detected.set_state(self.motion_detected.ON)
        self.motion_detected.publish_config_and_state(self.mqtt_client)

    @print_exception_decorator
    def callback_detection_cycle_ended(self):
        logger.debug(f'Detection Cycle Ended (UID: {self.device.uid_string})')
        self.motion_detected.set_state(self.motion_detected.OFF)
        self.motion_detected.publish_config_and_state(self.mqtt_client)
