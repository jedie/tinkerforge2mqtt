"""
    CLI for usage
"""

import asyncio
import logging
import os
import socket
import sys
import time
from datetime import datetime
from pathlib import Path

import rich_click as click
from bleak import AdvertisementData, BLEDevice
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE, setup_logging
from cli_base.cli_tools.version_info import print_version
from cli_base.systemd.api import ServiceControl
from cli_base.toml_settings.api import TomlSettings
from ha_services.mqtt4homeassistant.converter import values2mqtt_payload
from ha_services.mqtt4homeassistant.data_classes import HaValue, HaValues
from ha_services.mqtt4homeassistant.mqtt import HaMqttPublisher
from rich import print  # noqa
from rich.console import Console
from rich.traceback import install as rich_traceback_install
from rich_click import RichGroup
from victron_ble.devices import DeviceData
from victron_ble.exceptions import UnknownDeviceError
from victron_ble.scanner import BaseScanner, Scanner

import thinkerforge2mqtt
from thinkerforge2mqtt import constants
from thinkerforge2mqtt.user_settings import SystemdServiceInfo, UserSettings


logger = logging.getLogger(__name__)


OPTION_ARGS_DEFAULT_TRUE = dict(is_flag=True, show_default=True, default=True)
OPTION_ARGS_DEFAULT_FALSE = dict(is_flag=True, show_default=True, default=False)
ARGUMENT_EXISTING_DIR = dict(
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path)
)
ARGUMENT_NOT_EXISTING_DIR = dict(
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        readable=False,
        writable=True,
        path_type=Path,
    )
)
ARGUMENT_EXISTING_FILE = dict(
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, path_type=Path)
)


class ClickGroup(RichGroup):  # FIXME: How to set the "info_name" easier?
    def make_context(self, info_name, *args, **kwargs):
        info_name = './cli.py'
        return super().make_context(info_name, *args, **kwargs)


@click.group(
    cls=ClickGroup,
    epilog=constants.CLI_EPILOG,
)
def cli():
    pass


@click.command()
def version():
    """Print version and exit"""
    # Pseudo command, because the version always printed on every CLI call ;)
    sys.exit(0)


cli.add_command(version)


##################################################################################################


def get_settings() -> TomlSettings:
    return TomlSettings(
        dir_name='thinkerforge2mqtt',
        file_name='thinkerforge2mqtt',
        settings_dataclass=UserSettings(),
    )


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def edit_settings(verbosity: int):
    """
    Edit the settings file. On first call: Create the default one.
    """
    setup_logging(verbosity=verbosity)
    toml_settings: TomlSettings = get_settings()
    toml_settings.open_in_editor()


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def print_settings(verbosity: int):
    """
    Display (anonymized) MQTT server username and password
    """
    setup_logging(verbosity=verbosity)
    toml_settings: TomlSettings = get_settings()
    toml_settings.print_settings()


######################################################################################################
# Manage systemd service commands:


def get_systemd_settings(verbosity: int) -> SystemdServiceInfo:
    toml_settings: TomlSettings = get_settings()
    user_settings: UserSettings = toml_settings.get_user_settings(debug=verbosity > 0)
    systemd_settings: SystemdServiceInfo = user_settings.systemd
    return systemd_settings


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_debug(verbosity: int):
    """
    Print Systemd service template + context + rendered file content.
    """
    setup_logging(verbosity=verbosity)
    systemd_settings: SystemdServiceInfo = get_systemd_settings(verbosity)

    ServiceControl(info=systemd_settings).debug_systemd_config()


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_setup(verbosity: int):
    """
    Write Systemd service file, enable it and (re-)start the service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    systemd_settings: SystemdServiceInfo = get_systemd_settings(verbosity)

    ServiceControl(info=systemd_settings).setup_and_restart_systemd_service()


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_remove(verbosity: int):
    """
    Remove Systemd service file. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    systemd_settings: SystemdServiceInfo = get_systemd_settings(verbosity)

    ServiceControl(info=systemd_settings).remove_systemd_service()


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_status(verbosity: int):
    """
    Display status of systemd service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    systemd_settings: SystemdServiceInfo = get_systemd_settings(verbosity)

    ServiceControl(info=systemd_settings).status()


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def systemd_stop(verbosity: int):
    """
    Stops the systemd service. (May need sudo)
    """
    setup_logging(verbosity=verbosity)
    systemd_settings: SystemdServiceInfo = get_systemd_settings(verbosity)

    ServiceControl(info=systemd_settings).stop()


##################################################################################################


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE | {'default': 2})
def discover(verbosity: int):
    """
    Discover Victron devices with Instant Readout
    """
    setup_logging(verbosity=verbosity)

    class Scanner(BaseScanner):

        def callback(self, device: BLEDevice, advertisement: bytes):
            print(datetime.now())
            data = dict(name=device.name, address=device.address, details=device.details)
            print(data)

    async def scan():
        scanner = Scanner()
        await scanner.start()

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(scan())
    loop.run_forever()


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
@click.argument('mac', envvar='MAC', type=str, required=False, default=None)
@click.argument('key', envvar='KEY', type=str, required=False, default=None)
def debug_read(verbosity: int, mac: str = None, key: str = None):
    """
    Read data from specified devices and print them.
    MAC / KEY are used from config file, if not given.
    """
    toml_settings: TomlSettings = get_settings()
    user_settings: UserSettings = toml_settings.get_user_settings(debug=verbosity > 1)

    if not mac:
        mac = user_settings.device_address
    print(f'Use device MAC address: {mac!r}')

    if not key:
        key = user_settings.device_key
    print(f'Use device key: {key!r}')

    device_keys = {mac: key}

    async def scan(keys):
        scanner = Scanner(keys)
        await scanner.start()

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(scan(device_keys))
    loop.run_forever()


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE | {'default': 0})
def publish_loop(verbosity: int):
    """
    TODO: Publish MQTT messages in endless loop (Entrypoint from systemd)
    """
    toml_settings: TomlSettings = get_settings()
    user_settings: UserSettings = toml_settings.get_user_settings(debug=verbosity > 1)

    raise NotImplementedError


##################################################################################################


def main():
    print_version(thinkerforge2mqtt)

    console = Console()
    rich_traceback_install(
        width=console.size.width,  # full terminal width
        show_locals=True,
        suppress=[click],
        max_frames=2,
    )

    # Execute Click CLI:
    cli.name = './cli.py'
    cli()
