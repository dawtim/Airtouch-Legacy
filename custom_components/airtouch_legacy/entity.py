from __future__ import annotations

from homeassistant.helpers.entity import Entity


class AirTouchEntity(Entity):
    @property
    def device_info(self):
        return {
            "identifiers": {("airtouch_legacy", "controller")},
            "name": "AirTouch Controller",
            "manufacturer": "Polyaire",
            "model": "AirTouch Legacy / ZoneTouch",
        }
