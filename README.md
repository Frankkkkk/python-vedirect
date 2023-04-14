# python-VEDirect

## What is this lib ?
Small library to read Victron's VE.Direct frames.

This is useful in order to read Victron's MPPT charge controllers.

You need to use a VE.Direct to USB cable

## How to use this lib ?
First of all, install this library using pip:
```bash
pip3 install vedirect
```

Then, you simply need to import the lib and start asking values:
```python

>>> import vedirect
>>> device = vedirect.VEDirect()
>>> print(device.battery_volts)
27.5
```

The list of available parameters is:
```
battery_volts
battery_amps
solar_volts
solar_power
device_serial
device_MPPT_state
```
