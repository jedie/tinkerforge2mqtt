import logging

from ha_services.mqtt4homeassistant.components.switch import Switch
from paho.mqtt.client import Client
from tinkerforge.bricklet_industrial_dual_relay import BrickletIndustrialDualRelay

from tinkerforge2mqtt.device_map import register_map_class
from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase, print_exception_decorator


logger = logging.getLogger(__name__)


@register_map_class()
class BrickletIndustrialDualRelayMapper(DeviceMapBase):
    # https://www.tinkerforge.com/de/doc/Software/Bricklets/IndustrialDualRelay_Bricklet_Python.html

    device_identifier = BrickletIndustrialDualRelay.DEVICE_IDENTIFIER

    def __init__(self, *, device: BrickletIndustrialDualRelay, **kwargs):
        self.device: BrickletIndustrialDualRelay = device
        super().__init__(device=device, **kwargs)

    @print_exception_decorator
    def setup_sensors(self):
        super().setup_sensors()

        self.relay0_switch = Switch(
            device=self.mqtt_device,
            name='Relay 0',
            uid='relay0',
            callback=self.relay0_callback,
        )
        logger.info(f'Creating: {self.relay0_switch}')

        self.relay1_switch = Switch(
            device=self.mqtt_device,
            name='Relay 1',
            uid='relay1',
            callback=self.relay1_callback,
        )
        logger.info(f'Creating: {self.relay1_switch}')

    @print_exception_decorator
    def setup_callbacks(self):
        pass  # TODO

    @print_exception_decorator
    def poll(self):
        super().poll()

        relay0value, relay1value = self.device.get_value()

        if relay0value:
            self.relay0_switch.set_state(self.relay0_switch.ON)
        else:
            self.relay0_switch.set_state(self.relay0_switch.OFF)
        self.relay0_switch.publish_config_and_state(self.mqtt_client)

        if relay1value:
            self.relay1_switch.set_state(self.relay1_switch.ON)
        else:
            self.relay1_switch.set_state(self.relay1_switch.OFF)
        self.relay1_switch.publish_config_and_state(self.mqtt_client)

    @print_exception_decorator
    def relay0_callback(self, *, client: Client, component: Switch, old_state: str, new_state: str):
        logger.error(f'{component.name} relay 0 state changed: {old_state!r} -> {new_state!r}')
        turn_relay_on = new_state == self.relay0_switch.ON
        self.device.set_selected_value(channel=0, value=turn_relay_on)

        self.poll()

    @print_exception_decorator
    def relay1_callback(self, *, client: Client, component: Switch, old_state: str, new_state: str):
        logger.error(f'{component.name} relay 1 state changed: {old_state!r} -> {new_state!r}')
        turn_relay_on = new_state == self.relay1_switch.ON
        self.device.set_selected_value(channel=1, value=turn_relay_on)

        self.poll()
