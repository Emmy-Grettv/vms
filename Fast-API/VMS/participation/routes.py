from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Participation
from schemas import Participation as ParticipationSchema, ParticipationCreate as ParticipationCreateSchema
from database import get_db

router = APIRouter()

# Create a Participation
@router.post("/participations/", response_model=ParticipationSchema)
def create_participation(participation: ParticipationCreateSchema, db: Session = Depends(get_db)):
    db_participation = Participation(
        volunteer_id=participation.volunteer_id,
        event_id=participation.event_id,
        role=participation.role,
        status=participation.status,
        date_joined=participation.date_joined
    )
    db.add(db_participation)
    db.commit()
    db.refresh(db_participation)
    return db_participation

# Read All Participations for a Volunteer
@router.get("/participations/volunteer/{volunteer_id}", response_model=list[ParticipationSchema])
def get_participations_by_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    return db.query(Participation).filter(Participation.volunteer_id == volunteer_id).all()

# Read All Participations for an Event
@router.get("/participations/event/{event_id}", response_model=list[ParticipationSchema])
def get_participations_by_event(event_id: int, db: Session = Depends(get_db)):
    return db.query(Participation).filter(Participation.event_id == event_id).all()

# Delete a Participation
@router.delete("/participations/{volunteer_id}/{event_id}", response_model=ParticipationSchema)
def delete_participation(volunteer_id: int, event_id: int, db: Session = Depends(get_db)):
    db_participation = db.query(Participation).filter(
        Participation.volunteer_id == volunteer_id,
        Participation.event_id == event_id
    ).first()
    if db_participation is None:
        raise HTTPException(status_code=404, detail="Participation not found")
    
    db.delete(db_participation)
    db.commit()
    return db_participation
