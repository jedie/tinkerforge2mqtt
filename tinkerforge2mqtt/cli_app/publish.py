import logging
import time

import rich_click as click
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE
from ha_services.mqtt4homeassistant.mqtt import get_connected_client
from rich import print  # noqa
from rich import get_console
from tinkerforge.ip_connection import IPConnection

from tinkerforge2mqtt.cli_app import cli
from tinkerforge2mqtt.cli_app.settings import get_user_settings
from tinkerforge2mqtt.device_registry.devices_handler import DevicesHandler
from tinkerforge2mqtt.user_settings import UserSettings


logger = logging.getLogger(__name__)


def setup_logging(*, verbosity: int, log_format='%(message)s'):  # Move to cli_tools
    if verbosity == 0:
        level = logging.ERROR
    elif verbosity == 1:
        level = logging.WARNING
    elif verbosity == 2:
        level = logging.INFO
    else:
        level = logging.DEBUG
        if '%(name)s' not in log_format:
            log_format = f'(%(name)s) {log_format}'

    console = get_console()
    console.print(f'(Set log level {verbosity}: {logging.getLevelName(level)})', justify='right')
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt='[%x %X.%f]',
        # handlers=[
        #     RichHandler(console=console, omit_repeated_times=False,
        #     log_time_format='[%x FOO %X]'
        #
        # )],
        force=True,
    )


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE | {'default': 0})
def publish_loop(verbosity: int):
    """
    Publish Tinkerforge devices events via MQTT to Home Assistant.
    """
    setup_logging(verbosity=verbosity, log_format='%(levelname)s %(processName)s %(threadName)s %(message)s')
    user_settings: UserSettings = get_user_settings(verbosity=verbosity)

    # https://www.tinkerforge.com/en/doc/Software/IPConnection_Python.html
    ipcon = IPConnection()
    connect_kwargs = dict(
        host=user_settings.host,
        port=user_settings.port,
    )
    print(f'Connecting to {connect_kwargs}')
    ipcon.connect(**connect_kwargs)

    mqtt_client = get_connected_client(settings=user_settings.mqtt, verbosity=verbosity)
    mqtt_client.loop_start()

    devices_handler = DevicesHandler(ipcon, mqtt_client=mqtt_client, user_settings=user_settings)

    ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, devices_handler)

    while True:
        try:
            ipcon.enumerate()
            time.sleep(5)
        except KeyboardInterrupt:
            logger.info('Keyboard interrupt')
            ipcon.disconnect()
            break
