import logging
import time

from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Switch, SwitchInfo
from paho.mqtt.client import Client, MQTTMessage
from tinkerforge.bricklet_solid_state_relay_v2 import BrickletSolidStateRelayV2

from tinkerforge2mqtt.device_map import register_map_class
from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase, print_exception_decorator
from tinkerforge2mqtt.user_settings import UserSettings


logger = logging.getLogger(__name__)


@register_map_class()
class BrickletSolidStateRelayV2Mapper(DeviceMapBase):
    # https://www.tinkerforge.com/de/doc/Software/Bricklets/SolidStateRelayV2_Bricklet_Python.html

    device_identifier = BrickletSolidStateRelayV2.DEVICE_IDENTIFIER

    PAYLOAD_ON = 'ON'
    PAYLOAD_OFF = 'OFF'

    def __init__(
        self,
        *,
        device: BrickletSolidStateRelayV2,
        mqtt_settings: Settings.MQTT,
        user_settings: UserSettings,
    ):
        self.device: BrickletSolidStateRelayV2 = device
        super().__init__(device=device, mqtt_settings=mqtt_settings, user_settings=user_settings)

    @print_exception_decorator
    def setup_sensors(self):
        super().setup_sensors()
        return
        relay_info = SwitchInfo(
            name=f'Solid State Relay',
            unique_id=f'{self.user_settings.mqtt.unique_id_prefix}-relay_{self.device.uid_string}',
            device=self.device_info,
            payload_on=self.PAYLOAD_ON,
            payload_off=self.PAYLOAD_OFF,
        )
        logger.debug(f'Creating relay info: {relay_info}')
        relay_settings = Settings(mqtt=self.mqtt_settings, entity=relay_info)
        self.relay_switch = Switch(relay_settings, command_callback=self.relay_callback, user_data=None)
        logger.error(f'Creating: {self.relay_switch}')

    @print_exception_decorator
    def setup_callbacks(self):
        logger.warning(f'setup_callbacks {self}')
        with self._device_lock:
            super().setup_callbacks()
            return
            self.device.register_callback(self.device.CALLBACK_MONOFLOP_DONE, self.callback_monoflop_done)

    @print_exception_decorator
    def callback_monoflop_done(self, value):
        logger.warning(f'TODO: Monoflop Done: {value} (UID: {self.device.uid_string})')

    @print_exception_decorator
    def poll(self):
        super().poll()
        return
        state: bool = self.device.get_state()
        logger.warning(f'Polling {state=} from {self.relay_switch}')
        with self._device_lock:
            if state:
                self.relay_switch.on()
            else:
                self.relay_switch.off()

    @print_exception_decorator
    def relay_callback(self, client: Client, user_data, message: MQTTMessage):
        payload = message.payload.decode()
        logger.warning(f'Switch Callback: {client=} {user_data=} {payload=} (UID: {self.device.uid_string})')
        if payload == self.PAYLOAD_ON:
            state = True
        elif payload == self.PAYLOAD_OFF:
            state = False
        else:
            logger.error(f'Unknown payload: {payload=} (UID: {self.device.uid_string})')
            return

        with self._device_lock:
            self.device.set_state(state=state)
        time.sleep(0.1)
        self.poll()
