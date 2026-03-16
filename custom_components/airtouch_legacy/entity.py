from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity


class AirTouchEntity(CoordinatorEntity):
    @property
    def device_info(self):
        return {
            "identifiers": {("airtouch_legacy", "controller")},
            "name": "AirTouch Controller",
            "manufacturer": "Polyaire",
            "model": "AirTouch Legacy / ZoneTouch",
        }
