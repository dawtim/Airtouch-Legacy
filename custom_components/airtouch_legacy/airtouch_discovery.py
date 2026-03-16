from __future__ import annotations

import select
import socket
import time

from .const import DISCOVERY_PORT


def _parse_reply(payload: bytes):
    text = payload.decode("utf-8", errors="ignore").strip("\x00\r\n ")
    parts = [p.strip() for p in text.split(",")]
    if len(parts) >= 3 and parts[2].lower() == "airtouch":
        return {
            "host": parts[0],
            "device_id": parts[1],
            "product": parts[2],
            "raw": text,
        }
    return None


def passive_udp_discover(timeout: float = 2.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", DISCOVERY_PORT))
        sock.setblocking(False)
        end = time.time() + timeout
        while time.time() < end:
            ready, _, _ = select.select([sock], [], [], 0.2)
            if not ready:
                continue
            data, _addr = sock.recvfrom(1024)
            parsed = _parse_reply(data)
            if parsed:
                return parsed
    finally:
        sock.close()
    return None


def discover_controller():
    return passive_udp_discover()
