from __future__ import annotations


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

        # Best-effort damper command template derived from packet captures.
        frame = bytearray.fromhex(
            "55010c100000000000000000720000000000000000000000a08912440100000040d53b440100000080d53b4401000000c0d5"
        )

        # Best-effort encoded value seen changing between command families.
        frame[12] = 0x72 + max(0, min(100, percent))

        # Zone field is not fully decoded; retain the requested zone in a likely slot.
        frame[16] = zone & 0xFF

        return bytes(frame)

    @staticmethod
    def parse_status(data: bytes):
        if not data.startswith(AirTouchFrame.HEADER_RESPONSE):
            raise ValueError("Unexpected frame header")

        # Readback fields are not considered authoritative.
        return {
            "online": True,
            "raw_hex": data.hex(),
        }
