import inspect
import logging
import sys
import time
from pathlib import Path

import rich_click as click
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE, setup_logging
from rich import print  # noqa
from tinkerforge.device_factory import get_device_class
from tinkerforge.ip_connection import IPConnection

from tinkerforge2mqtt.cli_app import cli
from tinkerforge2mqtt.cli_app.settings import get_user_settings
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
        for name, func in inspect.getmembers(device, inspect.ismethod):
            if '_callback_' in name:
                continue

            if not (name.startswith('get_') or name.startswith('read_')):
                continue

            if name in ('get_bootloader_mode', 'read_uid'):
                continue

            spec = inspect.getfullargspec(func)
            if spec.args == ['self']:
                print(f'{name}():', end=' ')
                print(func())

    ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, enumerate_handler)
    ipcon.enumerate()
    time.sleep(2)
    ipcon.disconnect()
