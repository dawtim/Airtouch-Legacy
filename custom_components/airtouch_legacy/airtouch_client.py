import socket
from .const import DEFAULT_PORT
from .airtouch_protocol import AirTouchFrame

class AirTouchClient:
    def __init__(self, host: str, port: int = DEFAULT_PORT) -> None:
        self.host = host
        self.port = port

    def _send(self, packet: bytes) -> bytes:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((self.host, self.port))
            sock.sendall(packet)
            return sock.recv(4096)
        finally:
            sock.close()

    def poll(self):
        return AirTouchFrame.parse_status(self._send(AirTouchFrame.build_poll()))

    def set_zone(self, zone: int, enable: bool) -> None:
        self._send(AirTouchFrame.build_zone_command(zone, enable))

    def set_damper(self, zone: int, percent: int) -> None:
        self._send(AirTouchFrame.build_damper_command(zone, percent))
