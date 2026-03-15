from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, DEFAULT_PORT


class AirTouchConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            await self.async_set_unique_id(f"{user_input['host']}:{user_input['port']}")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"AirTouch {user_input['host']}:{user_input['port']}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("host"): str,
                    vol.Required("port", default=DEFAULT_PORT): int,
                }
            ),
        )
