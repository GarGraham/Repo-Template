from mvp.python.main import load_cfg
from mvp.python.app.pipeline import Pipeline
from mvp.python.adapters.source.mqtt import MqttSource

class DummySink:
    def __init__(self, *args, **kwargs):
        self.sent = []
    def send(self, payload: dict):
        self.sent.append(payload)
        return 200

def test_pipeline_smoke_no_network():
    cfg = load_cfg()
    src = MqttSource(cfg['source'])
    sink = DummySink()
    p = Pipeline(src, sink)
    p.run_once()
    assert len(sink.sent) == 1
    assert 'deviceId' in sink.sent[0]
