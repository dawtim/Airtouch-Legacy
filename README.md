# AirTouch Legacy

Custom HACS-compatible Home Assistant integration for legacy Polyaire AirTouch controllers.

## Current status

This package is narrowed to:
- exactly 6 zones
- zone on/off control
- zone damper percentage control
- default TCP port `8899`

It intentionally does **not** create climate or temperature entities.

## Important

This integration is still based on reverse-engineering from packet captures.
The network endpoint and poll frame are grounded in capture data, but zone field offsets and
write commands are still best-effort and may require further adjustment for your controller firmware.

## Entities created

- `switch.airtouch_zone_1` through `switch.airtouch_zone_6`
- `number.airtouch_zone_1_damper` through `number.airtouch_zone_6_damper`

## Installation

1. Add this repository to HACS as a custom repository, category **Integration**, or copy
   `custom_components/airtouch_legacy` into your Home Assistant config directory.
2. Restart Home Assistant.
3. Remove any previous AirTouch Legacy integration entry.
4. Add **AirTouch Legacy** again.
5. Enter the controller IP and port.

## Default port

The current default port is `8899`.
