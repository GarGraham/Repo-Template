from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceReading(BaseModel):
    device_id: str = Field(..., alias="deviceId")
    timestamp: datetime
    temperatureC: Optional[float] = None
    status: Optional[str] = None
