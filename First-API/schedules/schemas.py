from pydantic import BaseModel
from datetime import datetime

class ScheduleBase(BaseModel):
    volunteer_id: int
    event_id: int
    time_slot: datetime

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int

    class Config:
        orm_mode = True
