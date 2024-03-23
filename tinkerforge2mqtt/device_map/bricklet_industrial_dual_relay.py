import logging
import time

from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Switch, SwitchInfo
from paho.mqtt.client import Client, MQTTMessage
from tinkerforge.bricklet_industrial_dual_relay import BrickletIndustrialDualRelay

from tinkerforge2mqtt.device_map import register_map_class
from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase, print_exception_decorator
from tinkerforge2mqtt.user_settings import UserSettings


logger = logging.getLogger(__name__)


@register_map_class()
class BrickletIndustrialDualRelayMapper(DeviceMapBase):
    # https://www.tinkerforge.com/de/doc/Software/Bricklets/IndustrialDualRelay_Bricklet_Python.html

    device_identifier = BrickletIndustrialDualRelay.DEVICE_IDENTIFIER

    PAYLOAD_ON = 'ON'
    PAYLOAD_OFF = 'OFF'

    def __init__(
        self,
        *,
        device: BrickletIndustrialDualRelay,
        mqtt_settings: Settings.MQTT,
        user_settings: UserSettings,
    ):
        self.device: BrickletIndustrialDualRelay = device
        super().__init__(device=device, mqtt_settings=mqtt_settings, user_settings=user_settings)

    @print_exception_decorator
    def setup_sensors(self):
        super().setup_sensors()
        for index in (0, 1):
            relay_info = SwitchInfo(
                name=f'Relay {index}',
                unique_id=f'{self.user_settings.mqtt.unique_id_prefix}-relay{index}_{self.device.uid_string}',
                device=self.device_info,
                payload_on=self.PAYLOAD_ON,
                payload_off=self.PAYLOAD_OFF,
            )
            logger.debug(f'Creating relay info: {relay_info}')
            relay_settings = Settings(mqtt=self.mqtt_settings, entity=relay_info)
            relay_callback = getattr(self, f'relay_callback{index}')
            relay_switch = Switch(relay_settings, command_callback=relay_callback, user_data=None)
            logger.error(f'Creating: {relay_switch}')
            setattr(self, f'relay{index}_switch', relay_switch)
        self.relay0_switch: Switch
        self.relay1_switch: Switch

    @print_exception_decorator
    def setup_callbacks(self):
        with self._device_lock:
            super().setup_callbacks()
            self.device.register_callback(self.device.CALLBACK_MONOFLOP_DONE, self.callback_monoflop_done)

    @print_exception_decorator
    def callback_monoflop_done(self, value):
        logger.warning(f'TODO: Monoflop Done: {value} (UID: {self.device.uid_string})')

    @print_exception_decorator
    def poll(self):
        super().poll()
        values = self.device.get_value()  # e.g.: Value(channel0=False, channel1=False)
        for index, value in enumerate(values):
            relay_switch: Switch = getattr(self, f'relay{index}_switch')
            logger.warning(f'Polling {index=} {value=} {relay_switch}')
            with self._device_lock:
                if value:
                    relay_switch.on()
                else:
                    relay_switch.off()

    def _relay_callback(self, *, channel, message: MQTTMessage):
        payload = message.payload.decode()
        logger.warning(f'Switch Callback {channel=}: {payload=} (UID: {self.device.uid_string})')
        if payload == self.PAYLOAD_ON:
            turn_relay_on = True
        elif payload == self.PAYLOAD_OFF:
            turn_relay_on = False
        else:
            logger.error(f'Unknown payload: {payload=} ({channel=} UID: {self.device.uid_string})')
            return

        with self._device_lock:
            self.device.set_selected_value(channel=channel, value=turn_relay_on)
        time.sleep(0.1)
        self.poll()

    @print_exception_decorator
    def relay_callback0(self, client: Client, user_data, message: MQTTMessage):
        print('*'*300)
        logger.warning(f'TODO: Switch Callback 0 (UID: {self.device.uid_string})')
        self._relay_callback(channel=0, message=message)

    @print_exception_decorator
    def relay_callback1(self, client: Client, user_data, message: MQTTMessage):
        print('*' * 300)
        logger.warning(f'TODO: Switch Callback 1 (UID: {self.device.uid_string})')
        self._relay_callback(channel=1, message=message)
