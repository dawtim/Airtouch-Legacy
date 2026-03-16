from __future__ import annotations

from .const import DOMAIN, ZONE_STATE_OFFSET, ZONE_DAMPER_OFFSET, CHECKSUM_OFFSET


async def async_get_config_entry_diagnostics(hass, entry):
    store = hass.data[DOMAIN][entry.entry_id]
    coordinator = store["coordinator"]
    return {
        "controller_state": coordinator.data,
        "offsets": {
            "zone_state_offset": ZONE_STATE_OFFSET,
            "zone_damper_offset": ZONE_DAMPER_OFFSET,
            "checksum_offset": CHECKSUM_OFFSET,
        },
    }
