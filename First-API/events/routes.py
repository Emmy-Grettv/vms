from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from events import models, schemas

router = APIRouter()

# Create a new event
@router.post("/", response_model=schemas.Event)
def create_event(event: schemas.Event, db: Session = Depends(get_db)):
    db_event = models.Event(
        name=event.name, description=event.description, date=event.date
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

# Read all events
@router.get("/", response_model=schemas.EventsResponse)
def read_events(db: Session = Depends(get_db)):
    db_events = db.query(models.Event).all()
    if db_events:
        return {"message": "Events retrieved successfully", "events": db_events}
    raise HTTPException(status_code=404, detail="No events found")

# Read a single event by ID
@router.get("/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        return db_event
    raise HTTPException(status_code=404, detail="Event not found")

# Update an event by ID
@router.put("/{event_id}", response_model=schemas.Event)
def update_event(event_id: int, event: schemas.Event, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db_event.name = event.name
    db_event.description = event.description
    db_event.date = event.date
    db.commit()
    db.refresh(db_event)
    
    return db_event

# Delete an event by ID
@router.delete("/{event_id}", response_model=schemas.Event)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(db_event)
    db.commit()
    return db_event
