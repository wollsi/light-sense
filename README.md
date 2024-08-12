# LightSense

This little project aims to provide a small and handy tool to retro fit older devices that signal events via light (LEDs for example). To achive this we use a photo resistor and a small microcontroller to translate the light signal into "on" and "off". The change of state can then be processed further.

## Components

As microcontroller a D1 Mini (ESP8266 based) is used. The photo resistor is a GL5528 and additionally a 10kΩ resistor is needed.

## Basic layout

The basic layout of the circuit can be found as sketch on a breadboard in the following picture:

| ![Circuit on breadboard](circuit_breadboard.png "Circuit on breadboard") |
| -- |
| *This image was created with Fritzing* |

The red connections are the 3V3 connection, the blue one is ground. The yellow connection is transfering data (meassuring voltage) and the green one is needed to be able to wake from deepsleep.

## Software

As programming language [micropython](https://docs.micropython.org/en/latest/index.html) is used.

For more information about using micropython on the D1 mini see here: [Quick Start](https://docs.micropython.org/en/latest/esp8266/tutorial/index.html)

Micropython knows two special files:

- __[boot.py](code/boot.py)__ which is executed directly after booting.
- __[main.py](code/main.py)__ which is exectued after boot.py completes.

In this app boot.py is used to load the config parameters from config.json. The main.py holds the logic and executes after all config parameters are loaded.

## config.json

The config.json holds all parameters for easy configuration of the app.

```yaml
sleep_time=10000 # the milliseconds to sleep between each measurement
```

## Quick start

First assemble the circuit as shown above.

Connect the controller to your PC and install the firmware as described here: [Install micropython](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#getting-the-firmware)

Edit the [config.json](resources/config.json) and add the parameters you need.

To upload the files you can use [ampy](https://github.com/scientifichackers/ampy). Upload the following files:

- boot.py
- main.py
- data.txt
- config.json
