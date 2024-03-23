# import logging
#
# from ha_mqtt_discoverable import Settings
# from ha_mqtt_discoverable.sensors import Sensor, SensorInfo
# from tinkerforge.bricklet_temperature_v2 import BrickletTemperatureV2
#
# from tinkerforge2mqtt.device_map import register_map_class
# from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase, print_exception_decorator
#
#
# logger = logging.getLogger(__name__)
#
#
# @register_map_class()
# class BrickletTemperatureV2Mapper(DeviceMapBase):
#     # https://www.tinkerforge.com/de/doc/Software/Bricks/HATZero_Brick_Python.html
#
#     device_identifier = BrickletTemperatureV2.DEVICE_IDENTIFIER
#
#     def __init__(self, device: BrickletTemperatureV2, mqtt_settings: Settings.MQTT):
#         self.device: BrickletTemperatureV2 = device
#         super().__init__(device, mqtt_settings)
#
#     @print_exception_decorator
#     def setup_sensors(self):
#         super().setup_sensors()
#         temperature_sensor_info = SensorInfo(
#             name='Temperature',
#             unit_of_measurement='°C',
#             state_class='measurement',
#             device_class='temperature',
#             unique_id=f'temperature_{self.device.uid_string}',
#             device=self.device_info,
#         )
#         logger.info(f'Creating sensor: {temperature_sensor_info}')
#         temperature_sensor_settings = Settings(mqtt=self.mqtt_settings, entity=temperature_sensor_info)
#         self.usb_voltage_sensor = Sensor(settings=temperature_sensor_settings)
#         logger.info(f'Sensor: {self.usb_voltage_sensor}')
#         self.callback_temperature(value=self.device.get_temperature())
#
#     @print_exception_decorator
#     def setup_callbacks(self):
#         super().setup_callbacks()
#         self.device.set_temperature_callback_configuration(
#             period=1000,  # 1000ms == 1s
#             value_has_to_change=False,
#             option=BrickletTemperatureV2.THRESHOLD_OPTION_OFF,
#             min=-999,
#             max=999,
#         )
#         self.device.register_callback(self.device.CALLBACK_TEMPERATURE, self.callback_temperature)
#
#     @print_exception_decorator
#     def callback_temperature(self, value):
#         logger.debug(f'Temperature: {value / 100}°C (UID: {self.device.uid_string})')
#         self.usb_voltage_sensor.set_state(state=value / 100)
