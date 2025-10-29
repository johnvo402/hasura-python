from pydantic import BaseModel
from datetime import datetime

class ScheduleModel(BaseModel):
    id: str
    name: str
    payload: dict
    comment: str
    scheduled_time: datetime
    