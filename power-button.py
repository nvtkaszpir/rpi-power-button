#!/usr/bin/env python3

import os
import sys
import time
from signal import pause
from subprocess import check_call
from gpiozero import Button


# config section start

# set to True to not to really trigger system shutdown, but just print message
DEMO = bool(os.getenv('DEMO', default='True'))

# BCM GPIO pin to use, for example if you use GPIO27 then you type in here 27
# for reference see https://github.com/splitbrain/rpibplusleaf
BUTTON_GPIO_PIN = int(os.getenv('BUTTON_GPIO_PIN', default='27'))

# how long to keep key pressed to trigger shutdown function
KEY_HOLD_TIME_SECONDS = int(os.getenv('KEY_HOLD_TIME_SECONDS', default='2'))

# which led to control, on rpi3b+ led0 is green and usually assigned to mmc
# led1 is red and is assigned to power
LED = os.getenv('LED', default='led0')

# what kind of trigger to assign to led on start,
# to see all available triggers, run sudo cat /sys/class/leds/led0/trigger
# set to 'none' to keep it constantly bright on
TRIGGER_START = os.getenv('TRIGGER_START', default='none')

# what kind of trigger to assign to led on shutdown
# set it to 'timer' to blink
TRIGGER_SHUTDOWN = os.getenv('TRIGGER_SHUTDOWN', default='timer')

# config section end


def led_control(trigger, led):
    """
    Set specific led state based on trigger.

    Args:
        trigger (str): trigger name to apply to led
        led (str): led name

    """
    # change led status to specific trigger
    print(
        "led_control: setting trigger: '{trigger}' for led '{led}'...".format(
            trigger=trigger, led=led
        )
    )
    os.system(
        "echo {trigger} | sudo tee /sys/class/leds/{led}/trigger".format(
            trigger=trigger, led=led
        )
    )

    # sleep 1 second before another led control, otherwise it will not work
    time.sleep(1)

    # set led brightness so it is actually visible
    print("led_control: setting brightness 1 for led '{led}'...".format(led=led))
    os.system("echo 1 | sudo tee /sys/class/leds/{led}/brightness".format(led=led))

    sys.stdout.flush()


def shutdown(button):
    """
    Run shutdown command on button pressed.

    DEMO var controls if the actual shutdown command is executed.

    Notice: Must be single param passed, due to gpiozero docs.
    """
    print("Running shutdown due to key event on pin {}".format(button.pin))
    sys.stdout.flush()

    # set led status on shutdown
    led_control(TRIGGER_SHUTDOWN, LED)

    # run shutdown command
    if not DEMO:
        check_call(["sudo", "poweroff"])
    else:
        print("Running demo command...")
        check_call(["sudo", "date"])
        print("Done.")

    sys.stdout.flush()


def main():
    """
    Execute main key logic.

    You need to restart systemd service if you make any code changes.
    """
    print(
        "Registering button to BCM GPIO pin {}, key hold time {}s".format(
            BUTTON_GPIO_PIN, KEY_HOLD_TIME_SECONDS
        )
    )
    sys.stdout.flush()

    # set led status on start
    led_control(TRIGGER_START, LED)

    # register function on key press
    shutdown_btn = Button(BUTTON_GPIO_PIN, hold_time=KEY_HOLD_TIME_SECONDS)
    shutdown_btn.when_held = shutdown

    print("Running in demo mode: {}".format(DEMO))
    print("Starting event loop")
    sys.stdout.flush()  # flush output so that we can see messages in systemd

    # gpiozero pause() triggers infinite loop to listen to gpio events.
    pause()


if __name__ == "__main__":
    main()
