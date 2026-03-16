from __future__ import annotations

from .const import (
    ZONE_COUNT,
    ZONE_SWITCH_MAP,
    ZONE_STEP_MAP,
)


class AirTouchFrame:
    @staticmethod
    def checksum(frame: bytearray) -> int:
        return sum(frame[:12]) & 0xFF

    @staticmethod
    def build_init_packet() -> bytes:
        frame = bytearray(13)
        frame[0] = 0x55
        frame[1] = 0x00
        frame[2] = 0x0C
        frame[12] = AirTouchFrame.checksum(frame)
        return bytes(frame)

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
    def parse_state(data: bytes) -> dict:
        if not data:
            raise ValueError("Empty controller response")

        # Use the last 66fa frame if multiple chunks were concatenated.
        start = data.rfind(b"\x66\xfa")
        if start != -1:
            frame = data[start:]
        else:
            frame = data

        # Best-effort short-frame parser.
        # This does NOT claim the offsets are final.
        zones = []
        for i in range(ZONE_COUNT):
            base = 20 + (i * 8)
            enabled = False
            damper = 0

            if len(frame) > base + 2:
                enabled = bool(frame[base + 2])

            if len(frame) > base + 1:
                raw = frame[base + 1]
                # Clamp guessed readback into 0..100
                damper = max(0, min(100, int(raw)))

            zones.append(
                {
                    "id": i,
                    "enabled": enabled,
                    "damper": damper,
                    "damper_raw": frame[base + 1] if len(frame) > base + 1 else None,
                }
            )

        return {
            "zones": zones,
            "raw_hex": frame.hex(),
            "frame_len": len(frame),
        }
