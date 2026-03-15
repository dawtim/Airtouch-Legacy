from __future__ import annotations


class AirTouchFrame:
    HEADER_RESPONSE = b"\x66\xfa"

    @staticmethod
    def build_poll() -> bytes:
        return bytes.fromhex(
            "55010c020000000000000000640000000000000000000000a0099307010000004015bc07010000008015bc0701000000c015"
        )

    @staticmethod
    def build_zone_command(zone: int, enable: bool) -> bytes:
        payload = bytearray(16)
        payload[0] = zone & 0xFF
        payload[1] = 1 if enable else 0
        return bytes(bytearray([0x55]) + payload)

    @staticmethod
    def build_damper_command(zone: int, percent: int) -> bytes:
        payload = bytearray(16)
        payload[0] = zone & 0xFF
        payload[2] = max(0, min(100, percent))
        return bytes(bytearray([0x55]) + payload)

    @staticmethod
    def parse_status(data: bytes):
        if not data.startswith(AirTouchFrame.HEADER_RESPONSE):
            raise ValueError("Unexpected frame header")

        # Reverse-engineered best-effort field map
        zone_count = data[6] if len(data) > 6 else 0
        zones = []
        for i in range(zone_count):
            base = 20 + (i * 8)
            if len(data) <= base + 2:
                break
            zones.append(
                {
                    "id": i,
                    "name": f"Zone {i + 1}",
                    "temp": data[base],
                    "damper": data[base + 1],
                    "enabled": bool(data[base + 2]),
                }
            )

        return {
            "current_temp": data[10] if len(data) > 10 else None,
            "setpoint": data[11] if len(data) > 11 else None,
            "mode": data[12] if len(data) > 12 else None,
            "fan": data[13] if len(data) > 13 else None,
            "zone_count": zone_count,
            "zones": zones,
            "raw_hex": data.hex(),
        }
