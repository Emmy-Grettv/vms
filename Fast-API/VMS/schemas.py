from pydantic import BaseModel
from typing import Optional
from datetime import date, time

# Schema for Volunteer
class VolunteerBase(BaseModel):
    name: str
    email: str
    phone_number: str
    age: int
    skills: Optional[str] = None

class VolunteerCreate(VolunteerBase):
    pass

class Volunteer(VolunteerBase):
    volunteer_id: int

    class Config:
        orm_mode = True

# Schema for Event
class EventBase(BaseModel):
    name: str
    description: str
    location: str
    date: date
    time: time

class EventCreate(EventBase):
    pass

class Event(EventBase):
    event_id: int

    class Config:
        orm_mode = True

# Schema for Participation
class ParticipationBase(BaseModel):
    volunteer_id: int
    event_id: int
    role: Optional[str] = None
    status: Optional[str] = None
    date_joined: date

class ParticipationCreate(ParticipationBase):
    pass

class Participation(ParticipationBase):
    class Config:
        orm_mode = True
