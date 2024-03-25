import logging

from ha_services.mqtt4homeassistant.components.switch import Switch
from paho.mqtt.client import Client
from tinkerforge.bricklet_solid_state_relay_v2 import BrickletSolidStateRelayV2

from tinkerforge2mqtt.device_map import register_map_class
from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase, print_exception_decorator


logger = logging.getLogger(__name__)


@register_map_class()
class BrickletSolidStateRelayV2Mapper(DeviceMapBase):
    # https://www.tinkerforge.com/de/doc/Software/Bricklets/SolidStateRelayV2_Bricklet_Python.html

    device_identifier = BrickletSolidStateRelayV2.DEVICE_IDENTIFIER

    def __init__(self, *, device: BrickletSolidStateRelayV2, **kwargs):
        self.device: BrickletSolidStateRelayV2 = device
        super().__init__(device=device, **kwargs)

    @print_exception_decorator
    def setup_sensors(self):
        super().setup_sensors()

        self.relay_switch = Switch(
            device=self.mqtt_device,
            name='Relay',
            uid='relay',
            callback=self.relay_callback,
        )
        logger.info(f'Creating: {self.relay_switch}')

    @print_exception_decorator
    def setup_callbacks(self):
        logger.info(f'setup_callbacks {self}')
        super().setup_callbacks()

        self.device.register_callback(self.device.CALLBACK_MONOFLOP_DONE, self.callback_monoflop_done)

    @print_exception_decorator
    def callback_monoflop_done(self, value):
        logger.warning(f'TODO: Monoflop Done: {value} (UID: {self.device.uid_string})')

    @print_exception_decorator
    def poll(self):
        super().poll()

        state: bool = self.device.get_state()
        logger.info(f'Polling {state=} from {self.relay_switch}')
        if state:
            self.relay_switch.set_state(self.relay_switch.ON)
        else:
            self.relay_switch.set_state(self.relay_switch.OFF)
        self.relay_switch.publish_config_and_state(self.mqtt_client)

    @print_exception_decorator
    def relay_callback(self, *, client: Client, component: Switch, old_state: str, new_state: str):
        logger.error(f'{component.name} state changed: {old_state!r} -> {new_state!r}')
        if new_state == self.relay_switch.ON:
            self.device.set_state(True)
        else:
            self.device.set_state(False)

        self.poll()
