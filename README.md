# AirTouch Legacy

Custom HACS-compatible Home Assistant integration for legacy Polyaire AirTouch controllers.

## Current status

This package is narrowed to:
- exactly 6 zones
- damper percentage control only
- default TCP port `8899`

It intentionally does **not** create:
- climate entities
- temperature sensors
- zone switches

## Entities created

- `number.airtouch_zone_1_damper` through `number.airtouch_zone_6_damper`

## Important

This integration is based on reverse-engineering from packet captures.
The network endpoint and polling frame are grounded in capture data.
The damper write format is based on observed packet differences, but the readback offsets may still require adjustment for your exact controller firmware.

## Installation

1. Add this repository to HACS as a custom repository, category **Integration**, or copy
   `custom_components/airtouch_legacy` into your Home Assistant config directory.
2. Restart Home Assistant.
3. Remove any previous AirTouch Legacy integration entry.
4. Add **AirTouch Legacy** again.
5. Enter the controller IP and port.

## Default port

The current default port is `8899`.
