import logging

from cli_base.autodiscover import import_all_files
from tinkerforge.device_factory import DEVICE_CLASSES

from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase


logger = logging.getLogger(__name__)


class MapRegistry:
    def __init__(self):
        self._registry = {}

    def add_map_class(self, MapClass):
        logger.debug(f'Add map class: {MapClass}')
        assert issubclass(MapClass, DeviceMapBase), f'Class {MapClass} must be subclass of {DeviceMapBase}'
        device_identifier = MapClass.device_identifier
        assert device_identifier in DEVICE_CLASSES, f'Unknown device identifier: {device_identifier} from {MapClass}'
        self._registry[device_identifier] = MapClass

    def get_map_class(self, device_identifier) -> type[DeviceMapBase] | None:
        return self._registry.get(device_identifier)


map_registry = MapRegistry()


def register_map_class():
    """
    Decorator to add a new map class to the map registry.
    """

    def wrapper(MapClass):
        map_registry.add_map_class(MapClass)
        return MapClass

    return wrapper


# Register all map classes, just by import all files in this package:
import_all_files(package=__package__, init_file=__file__)
