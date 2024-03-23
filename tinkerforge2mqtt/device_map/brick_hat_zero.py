# import logging
#
# from ha_mqtt_discoverable import Settings
# from ha_mqtt_discoverable.sensors import Sensor, SensorInfo
# from tinkerforge.brick_hat_zero import BrickHATZero
#
# from tinkerforge2mqtt.device_map import register_map_class
# from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase, print_exception_decorator
#
#
# logger = logging.getLogger(__name__)
#
#
# @register_map_class()
# class BrickHATZeroMapper(DeviceMapBase):
#     # https://www.tinkerforge.com/de/doc/Software/Bricks/HATZero_Brick_Python.html
#
#     device_identifier = BrickHATZero.DEVICE_IDENTIFIER
#
#     def __init__(self, device: BrickHATZero, mqtt_settings: Settings.MQTT):
#         self.device: BrickHATZero = device
#         super().__init__(device, mqtt_settings)
#
#     @print_exception_decorator
#     def setup_sensors(self):
#         super().setup_sensors()
#         usb_voltage_sensor_info = SensorInfo(
#             name='USB Voltage',
#             unit_of_measurement='V',
#             state_class='measurement',
#             device_class='voltage',
#             unique_id=f'voltage_{self.device.uid_string}',
#             device=self.device_info,
#         )
#         logger.debug(f'Creating sensor info: {usb_voltage_sensor_info}')
#         usb_voltage_sensor_settings = Settings(mqtt=self.mqtt_settings, entity=usb_voltage_sensor_info)
#         self.usb_voltage_sensor = Sensor(settings=usb_voltage_sensor_settings)
#         logger.info(f'Sensor: {self.usb_voltage_sensor}')
#
#     @print_exception_decorator
#     def setup_callbacks(self):
#         super().setup_callbacks()
#         self.device.set_usb_voltage_callback_configuration(
#             period=1000,  # 1000ms == 1s
#             value_has_to_change=False,
#             option='x',  # Threshold is turned off
#             min=0,
#             max=999,
#         )
#         self.device.register_callback(BrickHATZero.CALLBACK_USB_VOLTAGE, self.callback_usb_voltage)
#         self.callback_usb_voltage(value=self.device.get_usb_voltage())
#
#     @print_exception_decorator
#     def callback_usb_voltage(self, value):
#         logger.debug(f'USB Voltage: {value / 1000}V (UID: {self.device.uid_string})')
#         self.usb_voltage_sensor.set_state(state=value / 1000)
