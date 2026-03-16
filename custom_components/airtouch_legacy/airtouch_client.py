from __future__ import annotations

import socket
import time

from .const import DEFAULT_PORT
from .airtouch_protocol import AirTouchFrame


class AirTouchClient:
    def __init__(self, host: str, port: int = DEFAULT_PORT) -> None:
        self.host = host
        self.port = port

    def _send(self, packet: bytes) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((self.host, self.port))
            sock.sendall(packet)
            try:
                sock.recv(256)
            except OSError:
                pass
        finally:
            sock.close()

    def step_damper(self, zone: int, direction: str) -> None:
        self._send(AirTouchFrame.build_step_command(zone, direction))

    def set_damper_absolute(self, zone: int, current_percent: int, target_percent: int) -> int:
        current_percent = max(0, min(100, int(current_percent)))
        target_percent = max(0, min(100, int(target_percent)))

        current_step = current_percent // 10
        target_step = target_percent // 10

        if target_step == current_step:
            return current_step * 10

        direction = "up" if target_step > current_step else "down"
        count = abs(target_step - current_step)

        for _ in range(count):
            self.step_damper(zone, direction)
            time.sleep(0.2)

        return target_step * 10
