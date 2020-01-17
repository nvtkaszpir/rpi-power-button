# Raspberry Pi 3 B+ shutdown button

## Requirements

- Python 3
- Raspberry Pi 3 (probably after some adjustments can work with other pi)

## Usage

1. install as in installation section below
2. adjust src/rpi-power-button/power-button.py top section and systemd files
3. restart systemd service
4. press desired gpio button, see if the shutdown trigger works as expected
5. revert from `DEMO` mode, restart service.

In default setup:

- when rpi turns on then green led is flashing for a moment,
  after system boot sequence is completed then led is constantly lit,
  no blinking
- when pressing key for 2s then shutdown function is executed,
  this will cause green led to start to blink slow, then it will blink
  faster (probably system thing), for a short time (1s?) it will
  glow without blinking and then finally led will be totally off
- when the green led is off it is safe to unplug the power from rpi

## Installation

- enable gpio in rpi3, see [luma-led-matrix docs](https://luma-led-matrix.readthedocs.io/en/latest/install.html)
- install deps, as follows

```bash
sudo usermod -a -G spi,gpio pi
sudo apt-get update
sudo apt-get install -y python3-gpiozero git

mkdir -p /home/pi/src
cd /home/pi/src/
git clone https://github.com/nvtkaszpir/rpi-power-button.git
cd rpi-power-button
sudo cp -f power-button.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable power-button
sudo systemctl start power-button
```

## Known limitations

- adjust files to your needs
- if your rpi is lacking power from power source then shutdown event
  may not be triggered - make sure you shut down device before power
  source is under certain threshold (there are special addons/hats for that)
- sometimes if your rpi is overloaded it may take more time to keep and hold
  the button to actually trigger shutdown
- your pull request may be rejected if I do not feel I need it

## Other

- code formatting with [black](https://github.com/psf/black)
