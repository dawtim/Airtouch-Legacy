# AirTouch Legacy

HACS-compatible Home Assistant integration for legacy Polyaire AirTouch / ZoneTouch controllers.

## v2.6.2 damper-only build

This build removes zone switches entirely and keeps only the working damper logic.

Included:
- TCP control on port `8899`
- UDP discovery on `48899`
- 6 non-optimistic damper controls
- live damper readback from the controller frame

Not included:
- zone switches
- climate entity
- temperature sensors

## Entities created

- `number.airtouch_zone_1_damper`
- `number.airtouch_zone_2_damper`
- `number.airtouch_zone_3_damper`
- `number.airtouch_zone_4_damper`
- `number.airtouch_zone_5_damper`
- `number.airtouch_zone_6_damper`

## Live frame parsing used in this build

Based on the live diagnostic frame:

- damper bytes: `309..314`

Damper values are interpreted as raw steps `0..10` and displayed as percentages `0..100`.

## Installation

1. Remove the old AirTouch integration entry
2. Replace the old `custom_components/airtouch_legacy` folder with this one
3. Restart Home Assistant
4. Add **AirTouch Legacy** again

## Note

This build intentionally removes the zone switch write path because it was not validated.
