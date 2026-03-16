from __future__ import annotations

from .const import COMMAND_HEADER, ZONE_STEP_MAP


class AirTouchFrame:
    @staticmethod
    def checksum(frame: bytearray) -> int:
        return sum(b & 0xFF for b in frame[:12]) & 0xFF

    @staticmethod
    def build_step_command(zone: int, direction: str) -> bytes:
        if zone not in ZONE_STEP_MAP:
            raise ValueError(f"Unsupported zone {zone}")

        byte_index, up_value, down_value = ZONE_STEP_MAP[zone]
        action_value = up_value if direction == "up" else down_value

        frame = bytearray(13)
        frame[0:3] = COMMAND_HEADER
        frame[byte_index] = action_value
        frame[12] = AirTouchFrame.checksum(frame)
        return bytes(frame)

    @staticmethod
    def build_init_packet() -> bytes:
        frame = bytearray(13)
        frame[0] = 0x55
        frame[1] = 0x00
        frame[2] = 0x0C
        frame[12] = AirTouchFrame.checksum(frame)
        return bytes(frame)
