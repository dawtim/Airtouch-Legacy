# AirTouch Legacy

Custom HACS-compatible Home Assistant integration for legacy Polyaire AirTouch controllers.

## Current status

This package is intentionally simplified to provide a predictable Home Assistant experience:

- exactly 6 zones
- damper percentage control only
- optimistic/write-only values
- 10% step size
- default TCP port `8899`

It does **not** create:
- climate entities
- temperature sensors
- zone switches

## Entities created

- `number.airtouch_zone_1_damper`
- `number.airtouch_zone_2_damper`
- `number.airtouch_zone_3_damper`
- `number.airtouch_zone_4_damper`
- `number.airtouch_zone_5_damper`
- `number.airtouch_zone_6_damper`

## Important

This integration is based on reverse-engineering from packet captures.

- The endpoint and polling traffic are grounded in captures.
- The controller readback for damper percentage is **not** reliably decoded.
- For that reason, this integration uses **optimistic values**: Home Assistant shows the last value you requested.

## Installation

1. Remove any previous AirTouch Legacy integration entry.
2. Replace the old `custom_components/airtouch_legacy` folder with this one.
3. Restart Home Assistant.
4. Add **AirTouch Legacy** again from **Settings → Devices & Services**.
5. Enter the controller IP and port.

## Default port

The current default port is `8899`.
