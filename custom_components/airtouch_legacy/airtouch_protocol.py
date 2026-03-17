from __future__ import annotations

from .const import ZONE_COUNT, ZONE_STEP_MAP, LIVE_DAMPER_OFFSET


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

        start = data.rfind(b"\x66\xfa")
        frame = data[start:] if start != -1 else data

        if len(frame) < LIVE_DAMPER_OFFSET + ZONE_COUNT:
            raise ValueError(f"State frame too short: {len(frame)}")

        zones = []
        for i in range(ZONE_COUNT):
            raw_damper = frame[LIVE_DAMPER_OFFSET + i]
            damper = max(0, min(100, int(raw_damper) * 10))
            zones.append({
                "id": i,
                "damper_raw": int(raw_damper),
                "damper": damper,
            })

        return {
            "zones": zones,
            "raw_hex": frame.hex(),
            "frame_len": len(frame),
        }
