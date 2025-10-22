from mvp.python.adapters.source.mqtt import MqttSource
from mvp.python.adapters.sink.http_push import HttpSink
from mvp.python.app.parse import parse_device_payload

class Pipeline:
    def __init__(self, source, sink):
        self.source = source; self.sink = sink
    def run_once(self):
        for raw in self.source.stream():
            reading = parse_device_payload(raw)
            self.sink.send(reading.model_dump(by_alias=False))

def build_from_config(cfg):
    return Pipeline(MqttSource(cfg['source']), HttpSink(cfg['sink']))
