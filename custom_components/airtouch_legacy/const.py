DOMAIN = "airtouch_legacy"
DEFAULT_PORT = 8899
DISCOVERY_PORT = 48899
ZONE_COUNT = 6
PLATFORMS = ["number"]

DEFAULT_DAMPER = 10
MIN_DAMPER = 0
MAX_DAMPER = 100
DAMPER_STEP = 10

COMMAND_HEADER = bytes([0x55, 0x01, 0x0C])

ZONE_STEP_MAP = {
    0: (3, 0x10, 0x20),
    1: (3, 0x01, 0x02),
    2: (4, 0x10, 0x20),
    3: (4, 0x01, 0x02),
    4: (5, 0x10, 0x20),
    5: (5, 0x01, 0x02),
}
