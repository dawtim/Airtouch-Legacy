import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class AirTouchConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            await self.async_set_unique_id(user_input["host"])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=f"AirTouch {user_input['host']}", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("host"): str}),
        )
