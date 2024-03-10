"""
    Allow thinkerforge2mqtt to be executable
    through `python -m thinkerforge2mqtt`.
"""


from thinkerforge2mqtt.cli import cli_app


def main():
    cli_app.main()


if __name__ == '__main__':
    main()
