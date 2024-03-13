import inspect
from collections.abc import Callable, Generator

from tinkerforge.ip_connection import Device


def iter_interest_functions(device: Device) -> Generator[Callable, None, None]:
    for name, func in inspect.getmembers(device, inspect.ismethod):
        if '_callback_' in name:
            continue

        if not name.startswith(('get_', 'read_')):
            continue

        if name in ('get_bootloader_mode', 'read_uid'):
            continue

        spec = inspect.getfullargspec(func)
        if spec.args == ['self']:
            yield func
