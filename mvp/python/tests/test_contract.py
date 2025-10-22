import json, pathlib
from mvp.python.app.models import DeviceReading

def test_golden_ok():
    data = json.loads(pathlib.Path('mvp/python/tests/golden/sample_ok.json').read_text())
    reading = DeviceReading.model_validate(data)
    assert reading.device_id and reading.timestamp

def test_golden_bad_fails():
    data = json.loads(pathlib.Path('mvp/python/tests/golden/sample_bad.json').read_text())
    try:
        DeviceReading.model_validate(data)
        assert False, "invalid payload should fail"
    except Exception:
        assert True
