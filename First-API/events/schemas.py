from pydantic import BaseModel
from datetime import datetime
from typing import List

class Event(BaseModel):
    id: int
    name: str
    description: str
    date: datetime

    class Config:
        orm_mode = True

class EventsResponse(BaseModel):
    message: str
    events: List[Event]
