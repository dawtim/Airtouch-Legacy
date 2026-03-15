from __future__ import annotations

from homeassistant.components.number import NumberEntity

from .const import DOMAIN
from .entity import AirTouchEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [AirTouchZoneDamper(coordinator, zone["id"]) for zone in coordinator.data.get("zones", [])]
    async_add_entities(entities)


class AirTouchZoneDamper(AirTouchEntity, NumberEntity):
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 5

    def __init__(self, coordinator, zone_id: int):
        super().__init__(coordinator)
        self.zone_id = zone_id
        self._attr_name = f"AirTouch Zone {zone_id + 1} Damper"

    @property
    def native_value(self):
        zones = self.coordinator.data.get("zones", [])
        if self.zone_id >= len(zones):
            return 0
        return zones[self.zone_id]["damper"]

    async def async_set_native_value(self, value: float):
        await self.hass.async_add_executor_job(
            self.coordinator.client.set_damper, self.zone_id, int(value)
        )
        await self.coordinator.async_request_refresh()

    @property
    def available(self):
        return self.coordinator.last_update_success
