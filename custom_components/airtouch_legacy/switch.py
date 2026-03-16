from __future__ import annotations

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN, ZONE_COUNT
from .entity import AirTouchEntity


async def async_setup_entry(hass, entry, async_add_entities):
    store = hass.data[DOMAIN][entry.entry_id]
    coordinator = store["coordinator"]
    client = store["client"]
    async_add_entities([AirTouchZoneSwitch(coordinator, client, zone_id) for zone_id in range(ZONE_COUNT)])


class AirTouchZoneSwitch(AirTouchEntity, SwitchEntity):
    def __init__(self, coordinator, client, zone_id: int):
        super().__init__(coordinator)
        self._client = client
        self.zone_id = zone_id
        self._attr_name = f"AirTouch Zone {zone_id + 1}"
        self._attr_unique_id = f"airtouch_legacy_zone_{zone_id + 1}_switch"

    @property
    def is_on(self):
        zones = self.coordinator.data.get("zones", [])
        if self.zone_id >= len(zones):
            return False
        return bool(zones[self.zone_id]["enabled"])

    async def async_turn_on(self, **kwargs):
        await self.hass.async_add_executor_job(self._client.send_zone, self.zone_id, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.hass.async_add_executor_job(self._client.send_zone, self.zone_id, False)
        await self.coordinator.async_request_refresh()

    @property
    def available(self):
        return self.coordinator.last_update_success
