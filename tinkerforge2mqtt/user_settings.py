import dataclasses
import sys

from cli_base.systemd.data_classes import BaseSystemdServiceInfo, BaseSystemdServiceTemplateContext
from ha_services.mqtt4homeassistant.data_classes import MqttSettings


@dataclasses.dataclass
class SystemdServiceTemplateContext(BaseSystemdServiceTemplateContext):
    """
    Context values for the systemd service file content.
    """

    verbose_service_name: str = 'tinkerforge2mqtt'
    exec_start: str = f'{sys.argv[0]} publish-loop'


@dataclasses.dataclass
class SystemdServiceInfo(BaseSystemdServiceInfo):
    """
    Information for systemd helper functions.
    """

    template_context: SystemdServiceTemplateContext = dataclasses.field(default_factory=SystemdServiceTemplateContext)


@dataclasses.dataclass
class UserSettings:
    """
    Tinkerforge -> MQTT - settings

    Note: Insert at least device address + key and your MQTT settings.

    See README for more information.
    """

    host: str = 'localhost'
    port: int = 4223

    callback_period: int = 1  # in seconds

    # Information about the MQTT server:
    mqtt: dataclasses = dataclasses.field(default_factory=MqttSettings)

    systemd: dataclasses = dataclasses.field(default_factory=SystemdServiceInfo)
