from __future__ import annotations

from .const import ZONE_COUNT


class AirTouchFrame:
    HEADER_RESPONSE = b"\x66\xfa"

    @staticmethod
    def build_poll() -> bytes:
        return bytes.fromhex(
            "55010c020000000000000000640000000000000000000000a0099307010000004015bc07010000008015bc0701000000c015"
        )

    @staticmethod
    def build_damper_command(zone: int, percent: int) -> bytes:
        percent = max(0, min(100, percent))

        frame = bytearray.fromhex(
            "55010c100000000000000000720000000000000001000000a049154c0100000040153c4c0100000080153c4c01000000c015"
        )

        # Reverse-engineered best-effort damper encoding from packet captures.
        frame[12] = 0x72 + percent

        return bytes(frame)

    @staticmethod
    def parse_status(data: bytes):
        if not data.startswith(AirTouchFrame.HEADER_RESPONSE):
            raise ValueError("Unexpected frame header")

        zones = []
        for i in range(ZONE_COUNT):
            base = 20 + (i * 8)
            if len(data) <= base + 1:
                break
            zones.append(
                {
                    "id": i,
                    "name": f"Zone {i + 1}",
                    "damper": data[base + 1],
                }
            )

        return {
            "zones": zones,
            "raw_hex": data.hex(),
        }
