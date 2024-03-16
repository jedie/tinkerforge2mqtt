import logging
import sys
import time
from pathlib import Path

import rich_click as click
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE, setup_logging
from rich import print  # noqa
from tinkerforge.device_factory import get_device_class
from tinkerforge.ip_connection import Error, IPConnection

from tinkerforge2mqtt.cli_app import cli
from tinkerforge2mqtt.cli_app.settings import get_user_settings
from tinkerforge2mqtt.device_map_utils.generics import iter_interest_functions
from tinkerforge2mqtt.device_registry.devices_handler import DevicesHandler
from tinkerforge2mqtt.user_settings import UserSettings


logger = logging.getLogger(__name__)


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE | {'default': 2})
def local_hat_info(verbosity: int):
    """
    Just print information about from `/proc/device-tree/hat/` files.
    """
    setup_logging(verbosity=verbosity)
    base_path = Path('/proc/device-tree/hat/')
    if not base_path.is_dir():
        print(f'ERROR: Path not found: {base_path}')
        sys.exit(-1)

    for file_path in base_path.glob('*'):
        try:
            content = file_path.read_text()
        except Exception:
            logger.exception(f'Can not read file {file_path}')
        else:
            print(f'{file_path.name}: {content}')


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE | {'default': 2})
def discover(verbosity: int):
    """
    Discover Victron devices with Instant Readout
    """
    setup_logging(verbosity=verbosity)
    user_settings: UserSettings = get_user_settings(verbosity=verbosity)

    # https://github.com/Tinkerforge/generators/tree/master/mqtt

    # https://www.tinkerforge.com/en/doc/Software/IPConnection_Python.html
    ipcon = IPConnection()
    connect_kwargs = dict(
        host=user_settings.host,
        port=user_settings.port,
    )
    print(f'Connecting to {connect_kwargs}')
    ipcon.connect(**connect_kwargs)

    def enumerate_handler(
        uid,
        connected_uid,
        position,
        hardware_version,
        firmware_version,
        device_identifier,
        enumeration_type,
    ):
        DeviceClass = get_device_class(device_identifier)
        print('_' * 80)
        print(f'{DeviceClass.DEVICE_DISPLAY_NAME} ({DeviceClass.__name__})')

        if enumeration_type == IPConnection.ENUMERATION_TYPE_DISCONNECTED:
            print('Disconnected!')
            return

        device = DeviceClass(uid=uid, ipcon=ipcon)

        for func in iter_interest_functions(device):
            name = func.__name__
            print(f'{name}():', end=' ')
            try:
                value = func()
            except Error as e:
                print(f'ERROR: {e}')
            else:
                print(value)

    ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, enumerate_handler)
    ipcon.enumerate()
    time.sleep(5)
    ipcon.disconnect()


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE | {'default': 2})
def discover_map(verbosity: int):
    """
    Discover Victron devices with Instant Readout
    """
    setup_logging(verbosity=verbosity)
    user_settings: UserSettings = get_user_settings(verbosity=verbosity)

    # https://github.com/Tinkerforge/generators/tree/master/mqtt

    # https://www.tinkerforge.com/en/doc/Software/IPConnection_Python.html
    ipcon = IPConnection()
    connect_kwargs = dict(
        host=user_settings.host,
        port=user_settings.port,
    )
    print(f'Connecting to {connect_kwargs}')
    ipcon.connect(**connect_kwargs)

    devices_handler = DevicesHandler(ipcon)

    ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, devices_handler)

    print('Aborting with Ctrl-C !')
    while True:
        try:
            ipcon.enumerate()
            time.sleep(5)
        except KeyboardInterrupt:
            logger.info('Keyboard interrupt')
            ipcon.disconnect()
            break
