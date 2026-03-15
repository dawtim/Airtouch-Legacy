# AirTouch Legacy

Custom HACS-compatible Home Assistant integration for legacy Polyaire AirTouch controllers (2012-2014) ZoneController..

NOTE this is still under development and not ready for public use



## Current status

This integration is based on reverse-engineering from packet captures supplied by the user.
It is configured for:

* Controller IP: user-specified
* Default TCP port: `8899`
* Request header: `0x55`
* Response header: `0x66FA`

## Features

* Config flow
* Climate entity
* Zone switches
* Zone temperature sensors
* Zone damper number entities
* Diagnostics support

## Important

The network endpoint and polling frame are grounded in packet captures.
The field layout for zone parsing and write commands remains reverse-engineered and may require adjustment for your exact controller firmware.

## Installation

1. Add this repository to HACS as a custom repository, category **Integration**, or copy `custom\_components/airtouch\_legacy` into your Home Assistant config directory.
2. Restart Home Assistant.
3. Go to **Settings → Devices \& Services → Add Integration**.
4. Add **AirTouch Legacy**.
5. Enter the controller IP and port.

## Default port

The current default port is `8899`.

