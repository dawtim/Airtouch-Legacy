from __future__ import annotations

from .const import DOMAIN, LIVE_ZONE_OFFSET, LIVE_DAMPER_OFFSET


async def async_get_config_entry_diagnostics(hass, entry):
    store = hass.data[DOMAIN][entry.entry_id]
    coordinator = store["coordinator"]
    return {
        "controller_state": coordinator.data,
        "offsets": {
            "live_zone_offset": LIVE_ZONE_OFFSET,
            "live_damper_offset": LIVE_DAMPER_OFFSET,
        },
    }
