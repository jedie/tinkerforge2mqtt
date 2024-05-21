from functools import wraps

from rich.console import Console


def print_exception_decorator(func):

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            console = Console()
            console.print_exception(show_locals=True)
            raise SystemExit from err

    return func_wrapper
