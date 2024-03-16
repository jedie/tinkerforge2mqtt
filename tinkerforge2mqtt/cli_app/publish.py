import logging
import time

import rich_click as click
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE, setup_logging
from ha_services.mqtt4homeassistant.mqtt import HaMqttPublisher
from rich import print  # noqa
from tinkerforge.ip_connection import IPConnection

from tinkerforge2mqtt.cli_app import cli
from tinkerforge2mqtt.cli_app.settings import get_user_settings
from tinkerforge2mqtt.device_registry.devices_handler import DevicesHandler
from tinkerforge2mqtt.user_settings import UserSettings


logger = logging.getLogger(__name__)


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE | {'default': 0})
def publish_loop(verbosity: int):
    """
    Discover Victron devices with Instant Readout
    """
    setup_logging(verbosity=verbosity)
    user_settings: UserSettings = get_user_settings(verbosity=verbosity)

    publisher = HaMqttPublisher(
        settings=user_settings.mqtt,
        verbosity=verbosity - 1,
        config_count=1,  # Send every time the config
    )

    # https://www.tinkerforge.com/en/doc/Software/IPConnection_Python.html
    ipcon = IPConnection()
    connect_kwargs = dict(
        host=user_settings.host,
        port=user_settings.port,
    )
    print(f'Connecting to {connect_kwargs}')
    ipcon.connect(**connect_kwargs)

    devices_handler = DevicesHandler(
        ipcon,
        publisher=publisher,
        name_prefix=user_settings.mqtt_payload_prefix,
        update_interval=user_settings.update_interval,
    )

    ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, devices_handler)

    print('Aborting with Ctrl-C !')
    while True:
        try:
            ipcon.enumerate()
            time.sleep(user_settings.enumerate_sleep)
        except Exception as err:
            logger.exception('Exception in enumerate loop: %s', err)
            break
        except KeyboardInterrupt:
            logger.info('Keyboard interrupt')
            ipcon.disconnect()
            break
