from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .airtouch_client import AirTouchClient
from .const import DOMAIN, PLATFORMS, ZONE_COUNT, DEFAULT_DAMPER


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    host = entry.data["host"]
    port = entry.data.get("port")

    client = AirTouchClient(host, port)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "values": {zone_id: DEFAULT_DAMPER for zone_id in range(ZONE_COUNT)},
        "discovery": {
            "host": host,
            "port": port,
            "method": entry.data.get("discovery_method", "manual"),
        },
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
