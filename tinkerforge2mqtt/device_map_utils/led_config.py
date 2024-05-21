import logging

from ha_services.mqtt4homeassistant.components import BaseComponent
from ha_services.mqtt4homeassistant.components.select import Select
from paho.mqtt.client import Client

from tinkerforge2mqtt.device_map_utils.utils import print_exception_decorator


logger = logging.getLogger(__name__)

CONFIG2LED_OPTIONS = {
    0: 'Off',
    1: 'On',
    2: 'Heartbeat',
    3: 'Status',
}
LED_OPTIONS2CONFIG = {v: k for k, v in CONFIG2LED_OPTIONS.items()}


class BrickletLedConfigSelect:
    def __init__(self, *, device, mqtt_device):
        self.device = device
        self.mqtt_device = mqtt_device

        current_config = self.device.get_status_led_config()

        self.led_config_select = Select(
            device=self.mqtt_device,
            name='LED Config',
            uid='led_config',
            callback=self.callback,
            options=tuple(CONFIG2LED_OPTIONS.values()),
            default_option=CONFIG2LED_OPTIONS[current_config],
        )

    @print_exception_decorator
    def poll(self, mqtt_client: Client):
        value = self.device.get_status_led_config()
        option = CONFIG2LED_OPTIONS[value]
        logger.info(f'{self.device.DEVICE_DISPLAY_NAME} status LED config: {value=} {option=}')
        self.led_config_select.set_state(state=option)
        self.led_config_select.publish(mqtt_client)

    def callback(self, *, client: Client, component: BaseComponent, old_state: str, new_state: str):
        logger.info(f'{component.name} state changed: {old_state!r} -> {new_state!r}')
        new_config = LED_OPTIONS2CONFIG[new_state]
        self.device.set_status_led_config(config=new_config)
        self.poll(mqtt_client=client)
