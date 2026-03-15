from __future__ import annotations

from .const import DOMAIN


async def async_get_config_entry_diagnostics(hass, entry):
    store = hass.data[DOMAIN][entry.entry_id]
    coordinator = store["coordinator"]
    return {
        "controller_state": coordinator.data,
        "optimistic_values": store["values"],
    }
