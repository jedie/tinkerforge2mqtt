# tinkerforge2mqtt

[![tests](https://github.com/jedie/tinkerforge2mqtt/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/tinkerforge2mqtt/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/tinkerforge2mqtt/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/tinkerforge2mqtt)
[![tinkerforge2mqtt @ PyPi](https://img.shields.io/pypi/v/tinkerforge2mqtt?label=tinkerforge2mqtt%20%40%20PyPi)](https://pypi.org/project/tinkerforge2mqtt/)
[![Python Versions](https://img.shields.io/pypi/pyversions/tinkerforge2mqtt)](https://github.com/jedie/tinkerforge2mqtt/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/tinkerforge2mqtt)](https://github.com/jedie/tinkerforge2mqtt/blob/main/LICENSE)

Stage: Planing...

## Usage

### Preperation

Setup APT repository for Tinkerforge: https://www.tinkerforge.com/doc/Software/APT_Repository.html

work-a-round for missing  `tinkerforge.asc` file:

```bash
wget -qO /tmp/tinkerforge.gpg https://download.tinkerforge.com/apt/$(. /etc/os-release; echo $ID)/tinkerforge.gpg
gpg  --keyring /tmp/temp.gpg  --no-default-keyring --import  /tmp/tinkerforge.gpg
gpg  --keyring /tmp/temp.gpg  --no-default-keyring  --export -a | sudo tee /etc/apt/trusted.gpg.d/tinkerforge.asc >/dev/null
rm -f /tmp/tinkerforge.gpg /tmp/temp.gpg
```
See: https://www.tinkerunity.org/topic/12201-fehler-beim-apt-quellen-einbinden/ (german)

Install Tinkerforge Brick Daemon: https://www.tinkerforge.com/doc/Software/Brickd.html

```bash
sudo apt install brickd
```



```bash

### Bootstrap

Clone the sources and just call the CLI to create a Python Virtualenv, e.g.:

```bash
~$ git clone https://github.com/jedie/tinkerforge2mqtt.git
~$ cd tinkerforge2mqtt
~/tinkerforge2mqtt$ ./cli.py --help
```

