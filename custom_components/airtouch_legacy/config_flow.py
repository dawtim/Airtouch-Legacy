from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries

from .airtouch_discovery import discover_controller
from .const import DOMAIN, DEFAULT_PORT


class AirTouchConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = (user_input.get("host") or "").strip()
            port = int(user_input.get("port", DEFAULT_PORT))
            auto_discover = bool(user_input.get("auto_discover", False))

            if auto_discover and not host:
                discovered = await self.hass.async_add_executor_job(discover_controller)
                if discovered:
                    host = discovered["host"]
                else:
                    errors["base"] = "cannot_connect"

            if host:
                await self.async_set_unique_id(f"{host}:{port}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"AirTouch {host}:{port}",
                    data={"host": host, "port": port},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional("host", default=""): str,
                    vol.Required("port", default=DEFAULT_PORT): int,
                    vol.Required("auto_discover", default=True): bool,
                }
            ),
            errors=errors,
        )
