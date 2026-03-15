from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature

from .const import DOMAIN
from .entity import AirTouchEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [AirTouchZoneTemp(coordinator, zone["id"]) for zone in coordinator.data.get("zones", [])]
    async_add_entities(entities)


class AirTouchZoneTemp(AirTouchEntity, SensorEntity):
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator, zone_id: int):
        super().__init__(coordinator)
        self.zone_id = zone_id
        self._attr_name = f"AirTouch Zone {zone_id + 1} Temperature"

    @property
    def native_value(self):
        return self.coordinator.data["zones"][self.zone_id]["temp"]

    @property
    def available(self):
        return self.coordinator.last_update_success
