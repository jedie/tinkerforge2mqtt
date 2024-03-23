import logging
import threading
import time
from pprint import pprint

import rich_click as click
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE
from rich import print  # noqa
from rich import get_console
from tinkerforge.ip_connection import IPConnection

from tinkerforge2mqtt.cli_app import cli
from tinkerforge2mqtt.cli_app.settings import get_user_settings
from tinkerforge2mqtt.device_registry.devices_handler import DevicesHandler
from tinkerforge2mqtt.user_settings import UserSettings


logger = logging.getLogger(__name__)


def setup_logging(*, verbosity: int, log_format='%(message)s'):
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
    Discover Victron devices with Instant Readout
    """
    setup_logging(verbosity=verbosity, log_format='%(levelname)s %(processName)s %(threadName)s %(message)s')
    user_settings: UserSettings = get_user_settings(verbosity=verbosity)
    pprint(user_settings)

    # https://www.tinkerforge.com/en/doc/Software/IPConnection_Python.html
    ipcon = IPConnection()

    devices_handler = DevicesHandler(
        ipcon,
        user_settings=user_settings,
    )

    ipcon.register_callback(IPConnection.CALLBACK_CONNECTED, devices_handler.connected_handler)
    ipcon.register_callback(IPConnection.CALLBACK_DISCONNECTED, devices_handler.disconnected_handler)
    ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, devices_handler.enumerate_handler)

    connect_kwargs = dict(
        host=user_settings.host,
        port=user_settings.port,
    )
    print(f'Connecting to {connect_kwargs}')
    ipcon.connect(**connect_kwargs)

    print('Aborting with Ctrl-C !')
    try:
        while True:
            print(f'{threading.active_count()=} {threading.current_thread()=}')
            ipcon.enumerate()
            time.sleep(3)
    except Exception as err:
        logger.exception('Exception in enumerate loop: %s', err)
    except KeyboardInterrupt:
        logger.info('Keyboard interrupt')
    ipcon.disconnect()
