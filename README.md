# tinkerforge2mqtt

[![tests](https://github.com/jedie/tinkerforge2mqtt/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/tinkerforge2mqtt/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/tinkerforge2mqtt/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/tinkerforge2mqtt)
[![tinkerforge2mqtt @ PyPi](https://img.shields.io/pypi/v/tinkerforge2mqtt?label=tinkerforge2mqtt%20%40%20PyPi)](https://pypi.org/project/tinkerforge2mqtt/)
[![Python Versions](https://img.shields.io/pypi/pyversions/tinkerforge2mqtt)](https://github.com/jedie/tinkerforge2mqtt/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/tinkerforge2mqtt)](https://github.com/jedie/tinkerforge2mqtt/blob/main/LICENSE)

Connect Tinkerforge Bricks/Bricklets via MQTT to Home Assistant...

Currently only a few Bricks/Bricklets are supported.
See existing [/tinkerforge2mqtt/device_map/](https://github.com/jedie/tinkerforge2mqtt/tree/main/tinkerforge2mqtt/device_map) files.

Forum threads:

* https://community.home-assistant.io/t/tinkerforge2mqtt-homeassistant/708678 (en)
* https://www.tinkerunity.org/topic/12220-tinkerforge2mqtt (de)

## Usage

### Preperation

Setup APT repository for Tinkerforge: https://www.tinkerforge.com/doc/Software/APT_Repository.html

Install Tinkerforge Brick Daemon: https://www.tinkerforge.com/doc/Software/Brickd.html

```bash
sudo apt install brickd
```


### Bootstrap tinkerforge2mqtt

Clone the sources and just call the CLI to create a Python Virtualenv, e.g.:

```bash
~$ git clone https://github.com/jedie/tinkerforge2mqtt.git
~$ cd tinkerforge2mqtt
~/tinkerforge2mqtt$ ./cli.py --help
```

[comment]: <> (✂✂✂ auto generated main help start ✂✂✂)
```
usage: ./cli.py [-h]
                {discover,discover-map,edit-settings,local-hat-info,print-settings,publish-loop,systemd-debug,systemd-
logs,systemd-remove,systemd-setup,systemd-status,systemd-stop,update-readme-history,version}



╭─ options ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help        show this help message and exit                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ {discover,discover-map,edit-settings,local-hat-info,print-settings,publish-loop,systemd-debug,systemd-logs,systemd │
│ -remove,systemd-setup,systemd-status,systemd-stop,update-readme-history,version}                                   │
│     discover      Discover Victron devices with Instant Readout                                                    │
│     discover-map  Discover Victron devices with Instant Readout                                                    │
│     edit-settings                                                                                                  │
│                   Edit the settings file. On first call: Create the default one.                                   │
│     local-hat-info                                                                                                 │
│                   Just print information about from `/proc/device-tree/hat/` files.                                │
│     print-settings                                                                                                 │
│                   Display (anonymized) MQTT server username and password                                           │
│     publish-loop  Publish Tinkerforge devices events via MQTT to Home Assistant.                                   │
│     systemd-debug                                                                                                  │
│                   Print Systemd service template + context + rendered file content.                                │
│     systemd-logs  Show systemd service logs. (May need sudo)                                                       │
│     systemd-remove                                                                                                 │
│                   Remove Systemd service file. (May need sudo)                                                     │
│     systemd-setup                                                                                                  │
│                   Write Systemd service file, enable it and (re-)start the service. (May need sudo)                │
│     systemd-status                                                                                                 │
│                   Display status of systemd service. (May need sudo)                                               │
│     systemd-stop  Stops the systemd service. (May need sudo)                                                       │
│     update-readme-history                                                                                          │
│                   Update project history base on git commits/tags in README.md Will be exited with 1 if the        │
│                   README.md was updated otherwise with 0.                                                          │
│                                                                                                                    │
│                   Also, callable via e.g.:                                                                         │
│                       python -m cli_base update-readme-history -v                                                  │
│     version       Print version and exit                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated main help end ✂✂✂)


## dev cli

[comment]: <> (✂✂✂ auto generated dev help start ✂✂✂)
```
usage: ./dev-cli.py [-h]
                    {coverage,install,lint,mypy,nox,pip-audit,publish,test,update,update-readme-history,update-test-sn
apshot-files,version}



╭─ options ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help        show this help message and exit                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ {coverage,install,lint,mypy,nox,pip-audit,publish,test,update,update-readme-history,update-test-snapshot-files,ver │
│ sion}                                                                                                              │
│     coverage      Run tests and show coverage report.                                                              │
│     install       Install requirements and 'tinkerforge2mqtt' via pip as editable.                                 │
│     lint          Check/fix code style by run: "ruff check --fix"                                                  │
│     mypy          Run Mypy (configured in pyproject.toml)                                                          │
│     nox           Run nox                                                                                          │
│     pip-audit     Run pip-audit check against current requirements files                                           │
│     publish       Build and upload this project to PyPi                                                            │
│     test          Run unittests                                                                                    │
│     update        Update dependencies (uv.lock) and git pre-commit hooks                                           │
│     update-readme-history                                                                                          │
│                   Update project history base on git commits/tags in README.md Will be exited with 1 if the        │
│                   README.md was updated otherwise with 0.                                                          │
│                                                                                                                    │
│                   Also, callable via e.g.:                                                                         │
│                       python -m cli_base update-readme-history -v                                                  │
│     update-test-snapshot-files                                                                                     │
│                   Update all test snapshot files (by remove and recreate all snapshot files)                       │
│     version       Print version and exit                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated dev help end ✂✂✂)


## Screenshots


# 2024-03-25tinkerforge2mqtt3.png

![2024-03-25tinkerforge2mqtt3.png](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/tinkerforge2mqtt/2024-03-25tinkerforge2mqtt3.png "2024-03-25tinkerforge2mqtt3.png")

# 2024-03-25tinkerforge2mqtt2.png

![2024-03-25tinkerforge2mqtt2.png](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/tinkerforge2mqtt/2024-03-25tinkerforge2mqtt2.png "2024-03-25tinkerforge2mqtt2.png")

# 2024-03-25tinkerforge2mqtt1.png

![2024-03-25tinkerforge2mqtt1.png](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/tinkerforge2mqtt/2024-03-25tinkerforge2mqtt1.png "2024-03-25tinkerforge2mqtt1.png")



[comment]: <> (✂✂✂ auto generated history start ✂✂✂)

* [v0.9.3](https://github.com/jedie/tinkerforge2mqtt/compare/v0.9.2...v0.9.3)
  * 2025-10-25 - Add PyCharm config files
  * 2025-10-25 - NEW: Show systemd service logs via CLI
* [v0.9.2](https://github.com/jedie/tinkerforge2mqtt/compare/v0.9.1...v0.9.2)
  * 2025-10-25 - Cleanup: Remove obsolete files
  * 2025-10-21 - switch to uv-python
  * 2025-09-20 - Update requirements
* [v0.9.1](https://github.com/jedie/tinkerforge2mqtt/compare/v0.9.0...v0.9.1)
  * 2024-05-23 - Update requirements
  * 2024-05-23 - Remove rich_traceback_install()
  * 2024-05-23 - Bugfix Dew Point sensor
  * 2024-05-21 - Add bricklet LED config and analog in oversampling to HA
* [v0.9.0](https://github.com/jedie/tinkerforge2mqtt/compare/v0.8.0...v0.9.0)
  * 2024-05-20 - BrickletHumidityV2Mapper: Calculate "dew point"
  * 2024-05-20 - fix huminity log message
  * 2024-05-20 - Update requirements

<details><summary>Expand older history entries ...</summary>

* [v0.8.0](https://github.com/jedie/tinkerforge2mqtt/compare/v0.7.0...v0.8.0)
  * 2024-04-12 - Add support for BrickletAnalogInV3
  * 2024-04-12 - Update requirements
* [v0.7.0](https://github.com/jedie/tinkerforge2mqtt/compare/v0.6.0...v0.7.0)
  * 2024-03-27 - Update to ha-services==2.5.0
* [v0.6.0](https://github.com/jedie/tinkerforge2mqtt/compare/v0.5.0...v0.6.0)
  * 2024-03-26 - Update to ha-services>=2.4.0
* [v0.5.0](https://github.com/jedie/tinkerforge2mqtt/compare/v0.4.0...v0.5.0)
  * 2024-03-26 - Update ha-services>=2.3.0
  * 2024-03-25 - Update README.md
* [v0.4.0](https://github.com/jedie/tinkerforge2mqtt/compare/v0.3.0...v0.4.0)
  * 2024-03-25 - Update README.md
  * 2024-03-25 - fix prefixing
* [v0.3.0](https://github.com/jedie/tinkerforge2mqtt/compare/v0.2.2...v0.3.0)
  * 2024-03-25 - Use "via-device" from ha-services v2.1
* [v0.2.2](https://github.com/jedie/tinkerforge2mqtt/compare/v0.2.1...v0.2.2)
  * 2024-03-24 - Update requirements e.g.: ha-services v2.0.1
* [v0.2.1](https://github.com/jedie/tinkerforge2mqtt/compare/v0.2.0...v0.2.1)
  * 2024-03-23 - Bugfix wrong values in VoltageCurrentV2 bricklet
* [v0.2.0](https://github.com/jedie/tinkerforge2mqtt/compare/v0.1.0...v0.2.0)
  * 2024-03-23 - Use new ha-services v2
* [v0.1.0](https://github.com/jedie/tinkerforge2mqtt/compare/c9fc77c...v0.1.0)
  * 2024-03-16 - fix publising
  * 2024-03-13 - Emit some MQTT events
  * 2024-03-12 - WIP
  * 2024-03-10 - first commit

</details>


[comment]: <> (✂✂✂ auto generated history end ✂✂✂)
