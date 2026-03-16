# AirTouch Legacy

HACS-compatible Home Assistant integration for legacy Polyaire AirTouch / ZoneTouch controllers.

## This build

This version is based on:
- live packet captures
- APK command logic
- real controller diagnostics from Home Assistant

It provides:
- TCP control on port `8899`
- UDP discovery on `48899`
- 6 real zone switches
- 6 real damper controls
- non-optimistic readback from the controller frame

## Important

This creates **12 entities total**, representing **6 zones**:

- `switch.airtouch_zone_1` ... `switch.airtouch_zone_6`
- `number.airtouch_zone_1_damper` ... `number.airtouch_zone_6_damper`

That is expected.

## Live frame parsing used in this build

Based on the live diagnostic frame you provided:

- zone bytes: `232..237`
- damper bytes: `309..314`

Damper values are interpreted as raw steps `0..10` and displayed as percentages `0..100`.

## Notes

This is the most grounded non-optimistic build so far, but if your controller firmware differs, the offsets may still need small adjustments.
