import json
from typing import Iterator
import time

class MqttSource:
    def __init__(self, cfg):
        self.cfg = cfg
    def stream(self) -> Iterator[dict]:
        # stub generator; swap with paho-mqtt
        while False:
            yield {}
        # for demo/testing, emit a single sample:
        yield {"deviceId":"demo-1","timestamp":"2025-01-01T00:00:00Z","temperatureC":21.5,"status":"OK"}
