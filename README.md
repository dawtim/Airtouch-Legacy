# AirTouch Legacy

HACS-compatible Home Assistant custom integration for legacy Polyaire AirTouch / ZoneTouch controllers.

## This build is based on APK logic

This package is based on reverse-engineering from the Android APK (`com.kmust.zonetouch`) and packet captures.

What is grounded in the APK:
- TCP port `8899`
- 13-byte command packets
- header bytes `55 01 0c`
- checksum in byte 12
- damper control is **step-based**, not absolute
- zone step commands are packed into bytes 3/4/5:
  - zone 1: byte 3, up `0x10`, down `0x20`
  - zone 2: byte 3, up `0x01`, down `0x02`
  - zone 3: byte 4, up `0x10`, down `0x20`
  - zone 4: byte 4, up `0x01`, down `0x02`
  - zone 5: byte 5, up `0x10`, down `0x20`
  - zone 6: byte 5, up `0x01`, down `0x02`

## What this integration does

- Creates 6 damper entities only
- Uses optimistic values in 10% steps
- Converts absolute slider changes into repeated APK-style up/down step commands

## What it does **not** do

- No climate entity
- No temperature sensors
- No zone on/off switches
- No controller readback parsing

## Entities created

- `number.airtouch_zone_1_damper`
- `number.airtouch_zone_2_damper`
- `number.airtouch_zone_3_damper`
- `number.airtouch_zone_4_damper`
- `number.airtouch_zone_5_damper`
- `number.airtouch_zone_6_damper`

## Installation

1. Remove any previous AirTouch Legacy integration entry
2. Replace the old `custom_components/airtouch_legacy` folder with this one
3. Restart Home Assistant
4. Add **AirTouch Legacy** again from **Settings → Devices & Services**
5. Enter the controller IP and port

## Notes

This version is intentionally conservative:
- it does not pretend to know true controller feedback
- it follows the APK's step-based damper model
- Home Assistant shows the last requested value
