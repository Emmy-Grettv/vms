from sqlalchemy import Column, Integer, DateTime, ForeignKey
from database import Base

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    time_slot = Column(DateTime)
