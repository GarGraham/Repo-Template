from .models import DeviceReading
from .transforms import rename_keys, unit_convert, enum_map

def parse_device_payload(raw: dict) -> DeviceReading:
    x = rename_keys(raw)
    x = unit_convert(x)
    x = enum_map(x)
    return DeviceReading.model_validate(x)
