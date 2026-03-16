from __future__ import annotations

from .const import (
    INIT_PACKET,
    ZONE_COUNT,
    ZONE_STATE_OFFSET,
    ZONE_DAMPER_OFFSET,
    CHECKSUM_OFFSET,
    STATE_MIN_LEN,
    ZONE_SWITCH_MAP,
    ZONE_STEP_MAP,
)


class AirTouchFrame:
    @staticmethod
    def checksum(frame: bytearray) -> int:
        return sum(frame[:12]) & 0xFF

    @staticmethod
    def build_init_packet() -> bytes:
        return INIT_PACKET

    @staticmethod
    def build_zone_switch(zone: int, turn_on: bool) -> bytes:
        if zone not in ZONE_SWITCH_MAP:
            raise ValueError(f"Unsupported zone {zone}")
        frame = bytearray(13)
        frame[0] = 0x55
        frame[1] = 0x01
        frame[2] = 0x0C
        index, on_value, off_value = ZONE_SWITCH_MAP[zone]
        frame[index] = on_value if turn_on else off_value
        frame[12] = AirTouchFrame.checksum(frame)
        return bytes(frame)

    @staticmethod
    def build_damper_step(zone: int, direction: str) -> bytes:
        if zone not in ZONE_STEP_MAP:
            raise ValueError(f"Unsupported zone {zone}")
        frame = bytearray(13)
        frame[0] = 0x55
        frame[1] = 0x01
        frame[2] = 0x0C
        index, up_value, down_value = ZONE_STEP_MAP[zone]
        frame[index] = up_value if direction == "up" else down_value
        frame[12] = AirTouchFrame.checksum(frame)
        return bytes(frame)

    @staticmethod
    def validate_state_frame(data: bytes) -> bool:
        if len(data) < STATE_MIN_LEN:
            return False
        checksum = sum(data[:CHECKSUM_OFFSET]) & 0xFF
        return checksum == data[CHECKSUM_OFFSET]

    @staticmethod
    def parse_state(data: bytes) -> dict:
        if len(data) < STATE_MIN_LEN:
            raise ValueError(f"State frame too short: {len(data)}")
        if not AirTouchFrame.validate_state_frame(data):
            raise ValueError("Invalid state checksum")

        zones = []
        for i in range(ZONE_COUNT):
            raw_state = data[ZONE_STATE_OFFSET + i]
            raw_damper = data[ZONE_DAMPER_OFFSET + i]
            zones.append({
                "id": i,
                "enabled": bool(raw_state),
                "damper_raw": raw_damper,
                "damper": max(0, min(100, int(raw_damper) * 10)),
            })

        return {
            "zones": zones,
            "raw_hex": data.hex(),
            "frame_len": len(data),
        }
