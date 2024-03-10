"""
    Allow tinkerforge2mqtt to be executable
    through `python -m tinkerforge2mqtt`.
"""


from tinkerforge2mqtt.cli import cli_app


def main():
    cli_app.main()


if __name__ == '__main__':
    main()
