DOMAIN = "airtouch_legacy"
DEFAULT_PORT = 8899
DISCOVERY_PORT = 48899
ZONE_COUNT = 6
PLATFORMS = ["switch", "number"]

MIN_DAMPER = 0
MAX_DAMPER = 100
DAMPER_STEP = 10

STATE_MIN_LEN = 0x146  # 326 bytes
ZONE_STATE_OFFSET = 0xE7
ZONE_DAMPER_OFFSET = 0x135
CHECKSUM_OFFSET = 0x145

INIT_PACKET = bytes([0x55, 0x00, 0x0C, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0x61])

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
