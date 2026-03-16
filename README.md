# AirTouch Legacy

HACS-compatible Home Assistant custom integration for legacy Polyaire AirTouch / ZoneTouch controllers.

## This build adds discovery support

What this package includes:
- TCP control on port `8899`
- UDP discovery support on port `48899`
- 6 damper entities only
- APK-derived 13-byte step commands
- optimistic 10% damper values

## Discovery behavior

On the config flow screen you can either:
- enter a host manually, or
- leave host blank and tick **Auto discover**

The integration will try:
1. passive UDP discovery on port `48899`
2. active UDP broadcast parsing for `ip,mac,AirTouch` replies
3. a light TCP 8899 scan fallback on the local `/24` subnet

## Notes

This package is still conservative:
- it does not parse true controller damper readback yet
- it follows the APK step-command logic for writes
- discovery is best-effort and may still require manual IP entry on some networks
