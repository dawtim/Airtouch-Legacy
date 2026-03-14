from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN
from .entity import AirTouchEntity

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [AirTouchZoneSwitch(coordinator, zone["id"]) for zone in coordinator.data.get("zones", [])]
    async_add_entities(entities)

class AirTouchZoneSwitch(AirTouchEntity, SwitchEntity):
    def __init__(self, coordinator, zone_id: int):
        super().__init__(coordinator)
        self.zone_id = zone_id
        self._attr_name = f"AirTouch Zone {zone_id + 1}"

    @property
    def is_on(self):
        return self.coordinator.data["zones"][self.zone_id]["enabled"]

    async def async_turn_on(self, **kwargs):
        await self.hass.async_add_executor_job(self.coordinator.client.set_zone, self.zone_id, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.hass.async_add_executor_job(self.coordinator.client.set_zone, self.zone_id, False)
        await self.coordinator.async_request_refresh()
