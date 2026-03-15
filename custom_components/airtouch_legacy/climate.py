from __future__ import annotations

from homeassistant.components.climate import ClimateEntity
from homeassistant.const import UnitOfTemperature

from .const import DOMAIN
from .entity import AirTouchEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AirTouchClimate(coordinator)])


class AirTouchClimate(AirTouchEntity, ClimateEntity):
    _attr_name = "AirTouch AC"
    _attr_temperature_unit = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator):
        super().__init__(coordinator)

    @property
    def current_temperature(self):
        return self.coordinator.data.get("current_temp")

    @property
    def target_temperature(self):
        return self.coordinator.data.get("setpoint")

    @property
    def available(self):
        return self.coordinator.last_update_success
