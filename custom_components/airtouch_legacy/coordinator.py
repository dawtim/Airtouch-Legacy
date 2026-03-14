from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

class AirTouchCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, client) -> None:
        super().__init__(
            hass,
            hass.logger,
            name="AirTouch",
            update_interval=timedelta(seconds=10),
        )
        self.client = client

    async def _async_update_data(self):
        return await self.hass.async_add_executor_job(self.client.poll)
