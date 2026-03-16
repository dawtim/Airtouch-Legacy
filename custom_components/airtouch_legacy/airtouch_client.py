from __future__ import annotations

import socket
import time

from .const import DEFAULT_PORT
from .airtouch_protocol import AirTouchFrame


class AirTouchClient:
    def __init__(self, host: str, port: int = DEFAULT_PORT) -> None:
        self.host = host
        self.port = port
        self.sock = None

    def connect(self) -> None:
        self.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2.0)
        self.sock.connect((self.host, self.port))

    def close(self) -> None:
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
        self.sock = None

    def ensure_connected(self) -> None:
        if self.sock is None:
            self.connect()

    def send(self, payload: bytes) -> None:
        self.ensure_connected()
        self.sock.sendall(payload)

    def send_init(self) -> None:
        self.send(AirTouchFrame.build_init_packet())

    def read_frame(self, window: float = 1.5) -> bytes:
        self.ensure_connected()
        self.sock.settimeout(0.2)
        deadline = time.time() + window
        chunks = []
        while time.time() < deadline:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                chunks.append(data)
            except socket.timeout:
                continue
        return b"".join(chunks)

    def fetch_state(self) -> dict:
        self.send_init()
        data = self.read_frame()
        return AirTouchFrame.parse_state(data)

    def send_zone(self, zone: int, enabled: bool) -> None:
        self.send(AirTouchFrame.build_zone_switch(zone, enabled))

    def step_damper(self, zone: int, direction: str) -> None:
        self.send(AirTouchFrame.build_damper_step(zone, direction))

    def set_damper_absolute(self, zone: int, current_percent: int, target_percent: int) -> None:
        current_step = max(0, min(10, int(current_percent) // 10))
        target_step = max(0, min(10, int(target_percent) // 10))
        direction = "up" if target_step > current_step else "down"
        count = abs(target_step - current_step)
        for _ in range(count):
            self.step_damper(zone, direction)
            time.sleep(0.15)
