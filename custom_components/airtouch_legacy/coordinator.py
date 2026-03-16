from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)


class AirTouchCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, client) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="AirTouch",
            update_interval=timedelta(seconds=15),
        )
        self.client = client

    async def _async_update_data(self):
        try:
            return await self.hass.async_add_executor_job(self.client.fetch_state)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with AirTouch controller: {err}") from err
