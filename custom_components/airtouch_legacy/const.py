DOMAIN = "airtouch_legacy"
DEFAULT_PORT = 8899
ZONE_COUNT = 6
PLATFORMS = ["number"]

DEFAULT_DAMPER = 10
MIN_DAMPER = 0
MAX_DAMPER = 100
DAMPER_STEP = 10

# APK-derived 13-byte command headers
COMMAND_HEADER = bytes([0x55, 0x01, 0x0C])

# zone_id: (payload_byte_index, up_value, down_value)
# payload starts at absolute byte 3 in the final 13-byte frame
ZONE_STEP_MAP = {
    0: (3, 0x10, 0x20),  # zone 1
    1: (3, 0x01, 0x02),  # zone 2
    2: (4, 0x10, 0x20),  # zone 3
    3: (4, 0x01, 0x02),  # zone 4
    4: (5, 0x10, 0x20),  # zone 5
    5: (5, 0x01, 0x02),  # zone 6
}
