# Raspberry Pi 3 B+ shutdown button

## Requirements

- Python 3
- Raspberry Pi 3 (probably after some adjustments can work with other pi)

## Usage

1. read this file from start to end :)
2. install as in installation section below
3. adjust environment vars of systemd files
4. restart systemd service
5. press desired gpio button, see if the shutdown trigger works as expected
6. revert from `DEMO` mode, restart service.

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

## Configuration

List of environmental vars used to control the app:

- `DEMO`: controls if the app executes real command to shutdown system
   or just prints generic message that the action was triggered.
   Set to 'True' or 'False', default is 'True' for easier debug.
   Given value is converted to boolean.
- `BUTTON_GPIO_PIN`: BCM GPIO pin number to use, converted to integer.
  For example if you use 'GPIO27' then you type in here '27'.
  For reference see [rpi b plus leaf](https://github.com/splitbrain/rpibplusleaf)
- `KEY_HOLD_TIME_SECONDS`: how many seconds key needs to be pressed
  so that action is triggered. This is to prevent accidental key presses.
  Converted to integer, defaults to '2'.
- `LED`: led name to use to change when action is triggered.
  Defaults to 'led0'.
  On rpi3b+ 'led0' is green and usually assigned to mmc card activity,
  while 'led1' is red and is assigned to power.
- `TRIGGER_START`: what kind of trigger to assign to led on start of app,
  to see all available triggers, run `sudo cat /sys/class/leds/led0/trigger`
  set to 'none' to keep it constantly bright on.
  Notice, this depends on current kernel on the rpi.
- `TRIGGER_SHUTDOWN`: what kind of trigger to assign to led on shutdown
  For example set it to 'timer' to blink once per second.
  To see all available triggers, run `sudo cat /sys/class/leds/led0/trigger`

You can override current systemd unit file by running command:

```bash
sudo systemctl edit --full power-button
```

This will create an override for default file.
Uncomment and edit desired `Environment` lines.

If overriden systemd file shows old content run daemon reload and delete file
`/etc/systemd/system/power-button.service` and try again.

After adjusting systemd unit file remember to run:

```bash
sudo systemctl daemon-reload
sudo systemctl restart power-button
```

To see the service logs, use for example:

```bash
sudo journalctl -u power-button -n 200 -f
```

## Known limitations

- adjust files to your needs manually
- on systemctl service stop the default led trigger is not restored,
  restart device to restore it.
- if your rpi is lacking power from power source then shutdown event
  may not be triggered - make sure you shut down device before power
  source is under certain threshold (there are special addons/hats for that)
- sometimes if your rpi is overloaded it may take more time to keep and hold
  the button to actually trigger shutdown
- your pull request may be rejected if I do not feel I need it

## Other

- code formatting with [black](https://github.com/psf/black)
