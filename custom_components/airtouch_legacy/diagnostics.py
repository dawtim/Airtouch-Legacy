from __future__ import annotations

from .const import DOMAIN, ZONE_STEP_MAP


async def async_get_config_entry_diagnostics(hass, entry):
    store = hass.data[DOMAIN][entry.entry_id]
    return {
        "optimistic_values": store["values"],
        "discovery": store["discovery"],
        "zone_step_map": ZONE_STEP_MAP,
        "notes": "UDP 48899 discovery plus APK-logic 13-byte TCP step commands.",
    }
