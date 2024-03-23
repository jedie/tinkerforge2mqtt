import random
import time

from ha_mqtt_discoverable import DeviceInfo, Settings
from ha_mqtt_discoverable.sensors import DeviceTrigger, DeviceTriggerInfo, Sensor, SensorInfo, Switch, SwitchInfo

from tinkerforge2mqtt.cli_app.publish import setup_logging
from tinkerforge2mqtt.cli_app.settings import get_user_settings
from tinkerforge2mqtt.user_settings import UserSettings


verbosity = 3
setup_logging(verbosity=verbosity, log_format='%(levelname)s %(processName)s %(threadName)s %(message)s')
user_settings: UserSettings = get_user_settings(verbosity=verbosity)


mqtt_settings = Settings.MQTT(
    host=user_settings.mqtt.host,
    port=user_settings.mqtt.port,
    username=user_settings.mqtt.user_name,
    password=user_settings.mqtt.password,
    client_name='test',
    discovery_prefix='homeassistant',
    state_prefix='homeassistant',
)


device_info = DeviceInfo(name="My device", identifiers="device_id")


def get_temperature_sensor():
    temperature_sensor = Sensor(
        Settings(
            mqtt=mqtt_settings,
            entity=SensorInfo(
                name='Chip Temperature',
                unit_of_measurement='°C',
                state_class='measurement',
                device_class='temperature',
                unique_id="temperature",
                device=device_info,
            ),
        )
    )
    temperature_sensor.set_state(state=random.randint(0, 100))
    return temperature_sensor


class Relay:
    def __init__(self):
        self.relay_switch = Switch(
            Settings(
                mqtt=mqtt_settings,
                entity=SwitchInfo(
                    name='Relay',
                    unique_id="relay",
                    device=device_info,
                    payload_on='ON',
                    payload_off='OFF',
                ),
            ),
            command_callback=self.relay_callback,
        )
        self.relay_switch.on()

    def relay_callback(self, client, user_data, message):
        payload = message.payload.decode()
        print(f'\n**** Switch Callback: {client=} {user_data=} {payload=}')
        if payload == 'ON':
            self.relay_switch.on()
        else:
            self.relay_switch.off()



# https://github.com/unixorn/ha-mqtt-discoverable
publish_relay1 = {
    'topic': 'homeassistant/switch/My-device/Relay/config',
    'payload': {
        "component": "switch",
        "device": {"name": "My device", "identifiers": "device_id"},
        "name": "Relay",
        "unique_id": "relay",
        "payload_off": "OFF",
        "payload_on": "ON",
        "state_topic": "homeassistant/switch/My-device/Relay/state",
        "json_attributes_topic": "homeassistant/switch/My-device/Relay/attributes",
        "command_topic": "homeassistant/switch/My-device/Relay/command",
    },
}
publish_relay2 = {'topic': 'homeassistant/switch/My-device/Relay/state', 'payload': 'ON'}
subscribe = {'topic': 'homeassistant/switch/My-device/Relay/command'}

publish_sensor1 = {
    'topic': 'homeassistant/sensor/My-device/Chip-Temperature/config',
    'payload': {
        "component": "sensor",
        "device": {"name": "My device", "identifiers": "device_id"},
        "device_class": "temperature",
        "name": "Chip Temperature",
        "unique_id": "temperature",
        "unit_of_measurement": "\\u00b0C",
        "state_class": "measurement",
        "state_topic": "homeassistant/sensor/My-device/Chip-Temperature/state",
        "json_attributes_topic": "homeassistant/sensor/My-device/Chip-Temperature/attributes",
    },
}
publish_sensor2 = {'topic': 'homeassistant/sensor/My-device/Chip-Temperature/state', 'payload': '40'}

relay = Relay()
temperature_sensor = get_temperature_sensor()

while True:
    time.sleep(1)
    print('.', end='', flush=True)
