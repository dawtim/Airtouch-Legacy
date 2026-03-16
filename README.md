# AirTouch Legacy

HACS-compatible Home Assistant integration for legacy Polyaire AirTouch / ZoneTouch controllers.

## This build

This package is based on the APK/socket logic and implements:

- TCP port `8899`
- UDP discovery on `48899`
- 13-byte control packets with checksum
- persistent TCP listener
- non-optimistic zone switch state
- non-optimistic damper state
- 6 zones

## State parsing used in this build

This build parses the large controller state frame using these APK-derived offsets:

- zone state bytes start at `0xE7`
- damper bytes start at `0x135`
- checksum byte at `0x145`

For the first 6 zones:
- zone state: bytes `0xE7` .. `0xEC`
- zone damper: bytes `0x135` .. `0x13A`

Damper values are interpreted as raw step values `0..10` and displayed as percentages `0..100`.

## Entities created

- `switch.airtouch_zone_1` ... `switch.airtouch_zone_6`
- `number.airtouch_zone_1_damper` ... `number.airtouch_zone_6_damper`

## Notes

This is the first non-optimistic/stateful build. If your controller firmware differs, offsets may still need adjustment.
