from __future__ import annotations

import ipaddress
import select
import socket
import time

from .const import DEFAULT_PORT, DISCOVERY_PORT
from .airtouch_protocol import AirTouchFrame


def _parse_reply(payload: bytes):
    try:
        text = payload.decode("utf-8", errors="ignore").strip("\x00\r\n ")
    except Exception:
        return None

    parts = [p.strip() for p in text.split(",")]
    if len(parts) >= 3 and parts[2].lower() == "airtouch":
        return {
            "host": parts[0],
            "device_id": parts[1],
            "product": parts[2],
            "raw": text,
        }
    return None


def passive_udp_discover(timeout: float = 2.0):
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


def active_udp_discover(timeout: float = 2.0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        recv.bind(("", DISCOVERY_PORT))
        recv.setblocking(False)

        # Best-effort broadcasts. Devices may reply to one of these depending on firmware.
        probes = [b"", b"admin", b"AirTouch", b"discover"]
        for probe in probes:
            try:
                sock.sendto(probe, ("255.255.255.255", DISCOVERY_PORT))
            except OSError:
                pass

        end = time.time() + timeout
        while time.time() < end:
            ready, _, _ = select.select([recv], [], [], 0.2)
            if not ready:
                continue
            data, _addr = recv.recvfrom(1024)
            parsed = _parse_reply(data)
            if parsed:
                return parsed
    finally:
        sock.close()
        recv.close()
    return None


def tcp_probe(host: str, timeout: float = 0.5) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, DEFAULT_PORT))
        sock.sendall(AirTouchFrame.build_init_packet())
        try:
            data = sock.recv(256)
        except OSError:
            data = b""
        return bool(data)
    except OSError:
        return False
    finally:
        sock.close()


def local_subnet_scan(timeout: float = 0.5):
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        net = ipaddress.ip_network(local_ip + "/24", strict=False)
    except Exception:
        return None

    for host in net.hosts():
        ip = str(host)
        if tcp_probe(ip, timeout=timeout):
            return {"host": ip, "device_id": "", "product": "AirTouch", "raw": "tcp_probe"}
    return None


def discover_controller():
    for fn in (passive_udp_discover, active_udp_discover, local_subnet_scan):
        result = fn()
        if result:
            return result
    return None
