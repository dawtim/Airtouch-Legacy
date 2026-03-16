from __future__ import annotations

from .const import DOMAIN, ZONE_STEP_MAP


async def async_get_config_entry_diagnostics(hass, entry):
    store = hass.data[DOMAIN][entry.entry_id]
    return {
        "optimistic_values": store["values"],
        "zone_step_map": ZONE_STEP_MAP,
        "notes": "APK-logic build: 13-byte step commands, optimistic values, no controller readback parsing.",
    }
