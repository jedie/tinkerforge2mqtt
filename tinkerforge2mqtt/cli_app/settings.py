import logging

from cli_base.cli_tools.verbosity import setup_logging
from cli_base.toml_settings.api import TomlSettings
from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print  # noqa

from tinkerforge2mqtt.cli_app import app
from tinkerforge2mqtt.user_settings import UserSettings


logger = logging.getLogger(__name__)


def get_toml_settings() -> TomlSettings:
    return TomlSettings(
        dir_name='tinkerforge2mqtt',
        file_name='tinkerforge2mqtt',
        settings_dataclass=UserSettings(),
    )


def get_user_settings(verbosity: TyroVerbosityArgType) -> UserSettings:
    toml_settings: TomlSettings = get_toml_settings()
    user_settings: UserSettings = toml_settings.get_user_settings(debug=verbosity > 0)
    return user_settings


@app.command
def edit_settings(verbosity: TyroVerbosityArgType):
    """
    Edit the settings file. On first call: Create the default one.
    """
    setup_logging(verbosity=verbosity)
    toml_settings: TomlSettings = get_toml_settings()
    toml_settings.open_in_editor()


@app.command
def print_settings(verbosity: TyroVerbosityArgType):
    """
    Display (anonymized) MQTT server username and password
    """
    setup_logging(verbosity=verbosity)
    toml_settings: TomlSettings = get_toml_settings()
    toml_settings.print_settings()
