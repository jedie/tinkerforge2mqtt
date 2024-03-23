# tinkerforge2mqtt

[![tests](https://github.com/jedie/tinkerforge2mqtt/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/tinkerforge2mqtt/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/tinkerforge2mqtt/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/tinkerforge2mqtt)
[![tinkerforge2mqtt @ PyPi](https://img.shields.io/pypi/v/tinkerforge2mqtt?label=tinkerforge2mqtt%20%40%20PyPi)](https://pypi.org/project/tinkerforge2mqtt/)
[![Python Versions](https://img.shields.io/pypi/pyversions/tinkerforge2mqtt)](https://github.com/jedie/tinkerforge2mqtt/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/tinkerforge2mqtt)](https://github.com/jedie/tinkerforge2mqtt/blob/main/LICENSE)

Connect Tinkerforge Bricks/Bricklets via MQTT to Home Assistant...

Currently only a few Bricks/Bricklets are supported.
See existing [/tinkerforge2mqtt/device_map/](https://github.com/jedie/tinkerforge2mqtt/tree/main/tinkerforge2mqtt/device_map) files.


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


## Screenshots


![2024-03-23tinkerforge2mqtt1.png](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/tinkerforge2mqtt/2024-03-23tinkerforge2mqtt1.png "2024-03-23tinkerforge2mqtt1.png")
