import inspect
from unittest import TestCase

from tinkerforge2mqtt.mapping.value_map import HaValueInfo, ValueMap


DEVICE_CLASSES = {
    'date',
    'enum',
    'timestamp',
    'apparent_power',
    'aqi',
    'atmospheric_pressure',
    'battery',
    'carbon_monoxide',
    'carbon_dioxide',
    'current',
    'data_rate',
    'data_size',
    'distance',
    'duration',
    'energy',
    'energy_storage',
    'frequency',
    'gas',
    'humidity',
    'illuminance',
    'irradiance',
    'moisture',
    'monetary',
    'nitrogen_dioxide',
    'nitrogen_monoxide',
    'nitrous_oxide',
    'ozone',
    'ph',
    'pm1',
    'pm10',
    'pm25',
    'power_factor',
    'power',
    'precipitation',
    'precipitation_intensity',
    'pressure',
    'reactive_power',
    'signal_strength',
    'sound_pressure',
    'speed',
    'sulphur_dioxide',
    'temperature',
    'volatile_organic_compounds',
    'volatile_organic_compounds_parts',
    'voltage',
    'volume',
    'volume_storage',
    'volume_flow_rate',
    'water',
    'weight',
    'wind_speed',
}


class ValueMapTestCase(TestCase):
    def test_valuemap(self):
        def is_ha_value_info(value):
            return isinstance(value, HaValueInfo)

        for name, value in inspect.getmembers(ValueMap, is_ha_value_info):
            with self.subTest(name=name):
                if device_class := value.device_class:
                    self.assertIn(device_class, DEVICE_CLASSES)
