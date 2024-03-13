import dataclasses

from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase
from tinkerforge2mqtt.mapping.value_map import HaValueInfo


@dataclasses.dataclass
class DeviceValue:
    device_mapper: DeviceMapBase
    value: int | float | str
    info: HaValueInfo
