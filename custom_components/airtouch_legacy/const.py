DOMAIN = "airtouch_legacy"
DEFAULT_PORT = 8899
DISCOVERY_PORT = 48899
ZONE_COUNT = 6
PLATFORMS = ["switch", "number"]

MIN_DAMPER = 0
MAX_DAMPER = 100
DAMPER_STEP = 10

LIVE_ZONE_OFFSET = 232
LIVE_DAMPER_OFFSET = 309

# zone_id: (payload_byte_index, on_value, off_value)
ZONE_SWITCH_MAP = {
    0: (3, 0x80, 0x40),
    1: (3, 0x08, 0x04),
    2: (4, 0x80, 0x40),
    3: (4, 0x08, 0x04),
    4: (5, 0x80, 0x40),
    5: (5, 0x08, 0x04),
}

# zone_id: (payload_byte_index, up_value, down_value)
ZONE_STEP_MAP = {
    0: (3, 0x10, 0x20),
    1: (3, 0x01, 0x02),
    2: (4, 0x10, 0x20),
    3: (4, 0x01, 0x02),
    4: (5, 0x10, 0x20),
    5: (5, 0x01, 0x02),
}
