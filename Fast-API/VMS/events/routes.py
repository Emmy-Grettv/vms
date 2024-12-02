from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Event
from schemas import Event as EventSchema, EventCreate as EventCreateSchema
from database import get_db

router = APIRouter()

# Create an Event
@router.post("/events/", response_model=EventSchema)
def create_event(event: EventCreateSchema, db: Session = Depends(get_db)):
    db_event = Event(
        name=event.name,
        description=event.description,
        location=event.location,
        date=event.date,
        time=event.time
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

# Read All Events
@router.get("/events/", response_model=list[EventSchema])
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

# Read Specific Event by ID
@router.get("/events/{event_id}", response_model=EventSchema)
def get_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

# Update an Event
@router.put("/events/{event_id}", response_model=EventSchema)
def update_event(event_id: int, event: EventCreateSchema, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db_event.name = event.name
    db_event.description = event.description
    db_event.location = event.location
    db_event.date = event.date
    db_event.time = event.time
    db.commit()
    db.refresh(db_event)
    return db_event

# Delete an Event
@router.delete("/events/{event_id}", response_model=EventSchema)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(db_event)
    db.commit()
    return db_event
