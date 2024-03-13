import dataclasses

from ha_services.mqtt4homeassistant.data_classes import HaValue


@dataclasses.dataclass
class HaValueInfo:
    name: str
    device_class: str | None  # e.g.: "voltage" / "current" / "energy" etc.
    state_class: str | None  # e.g.: "measurement" / "total" / "total_increasing" etc.
    unit: str | None  # e.g.: "V" / "A" / "kWh" etc.

    def get_log_message(self, device, value):
        return f'{self.name}: {value} {self.unit} [{device.DEVICE_DISPLAY_NAME} ({device.uid_string})]'

    def get_ha_value(self, value) -> HaValue:
        return HaValue(
            name=self.name,
            value=value,
            device_class=self.device_class,
            state_class=self.state_class,
            unit=self.unit,
        )


class ValueMap:
    API_VERSION = HaValueInfo(
        name='API Version',
        device_class=None,
        state_class='firmware',
        unit=None,
    )
    USB_VOLTAGE = HaValueInfo(
        name='USB Voltage',
        device_class='voltage',
        state_class='measurement',
        unit='V',
    )
    TEMPERATURE = HaValueInfo(
        name='Temperature',
        device_class='temperature',
        state_class='measurement',
        unit='°C',
    )
    CHIP_TEMPERATURE = HaValueInfo(
        name='Chip Temperature',
        device_class='temperature',
        state_class='measurement',
        unit='°C',
    )
    STATUS_LED_CONFIG = HaValueInfo(
        name='Status LED Config',
        device_class='enum',
        state_class=None,
        unit=None,
    )
    MOTION_DETECTED = HaValueInfo(
        name='Motion detected',
        device_class=None,
        state_class='motion',
        unit=None,
    )
    DETECTION_CYCLE_ENDED = HaValueInfo(
        name='Detection Cycle Ended',
        device_class=None,
        state_class='motion',
        unit=None,
    )
    PIR_SENSOR_SENSITIVITY = HaValueInfo(
        name='Sensitivity of the PIR sensor',
        device_class='weight',
        state_class='measurement',
        unit='%',
    )
