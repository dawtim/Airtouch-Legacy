from __future__ import annotations

from homeassistant.components.number import NumberEntity

from .const import DOMAIN
from .entity import AirTouchEntity


async def async_setup_entry(hass, entry, async_add_entities):
    store = hass.data[DOMAIN][entry.entry_id]
    coordinator = store["coordinator"]
    entities = [AirTouchZoneDamper(coordinator, store["values"], zone_id) for zone_id in range(6)]
    async_add_entities(entities)


class AirTouchZoneDamper(AirTouchEntity, NumberEntity):
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 10

    def __init__(self, coordinator, value_store: dict, zone_id: int):
        super().__init__(coordinator)
        self.zone_id = zone_id
        self._values = value_store
        self._attr_name = f"AirTouch Zone {zone_id + 1} Damper"

    @property
    def native_value(self):
        return self._values.get(self.zone_id, 10)

    async def async_set_native_value(self, value: float):
        value = max(0, min(100, int(value)))
        await self.hass.async_add_executor_job(
            self.coordinator.client.set_damper, self.zone_id, value
        )
        self._values[self.zone_id] = value
        self.async_write_ha_state()

    @property
    def available(self):
        return self.coordinator.last_update_success
