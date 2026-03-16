from __future__ import annotations

from homeassistant.components.number import NumberEntity

from .const import DOMAIN, ZONE_COUNT, MIN_DAMPER, MAX_DAMPER, DAMPER_STEP
from .entity import AirTouchEntity


async def async_setup_entry(hass, entry, async_add_entities):
    store = hass.data[DOMAIN][entry.entry_id]
    coordinator = store["coordinator"]
    client = store["client"]
    async_add_entities([AirTouchZoneDamper(coordinator, client, zone_id) for zone_id in range(ZONE_COUNT)])


class AirTouchZoneDamper(AirTouchEntity, NumberEntity):
    _attr_native_min_value = MIN_DAMPER
    _attr_native_max_value = MAX_DAMPER
    _attr_native_step = DAMPER_STEP

    def __init__(self, coordinator, client, zone_id: int):
        super().__init__(coordinator)
        self._client = client
        self.zone_id = zone_id
        self._attr_name = f"AirTouch Zone {zone_id + 1} Damper"
        self._attr_unique_id = f"airtouch_legacy_zone_{zone_id + 1}_damper"

    @property
    def native_value(self):
        zones = self.coordinator.data.get("zones", [])
        if self.zone_id >= len(zones):
            return 0
        return int(zones[self.zone_id]["damper"])

    async def async_set_native_value(self, value: float):
        target = max(0, min(100, int(value)))
        current = int(self.native_value)
        await self.hass.async_add_executor_job(
            self._client.set_damper_absolute,
            self.zone_id,
            current,
            target,
        )
        await self.coordinator.async_request_refresh()

    @property
    def available(self):
        return self.coordinator.last_update_success
