from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Volunteer(Base):
    __tablename__ = 'volunteers'

    volunteer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    age = Column(Integer)
    skills = Column(String, nullable=True)

    participations = relationship("Participation", back_populates="volunteer")

# Event Model
class Event(Base):
    __tablename__ = 'events'

    event_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    location = Column(String)
    date = Column(Date)
    time = Column(Time)

    participations = relationship("Participation", back_populates="event")

# Participation Model (Join Table)
class Participation(Base):
    __tablename__ = 'participations'

    volunteer_id = Column(Integer, ForeignKey('volunteers.volunteer_id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'), primary_key=True)
    role = Column(String, nullable=True)
    status = Column(String, nullable=True)
    date_joined = Column(Date)

    volunteer = relationship("Volunteer", back_populates="participations")
    event = relationship("Event", back_populates="participations")
