from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schedules import models, schemas
from database import get_db

router = APIRouter()

# Create a new schedule (POST /schedules/)
@router.post("/", response_model=schemas.Schedule)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = models.Schedule(volunteer_id=schedule.volunteer_id, event_id=schedule.event_id, time_slot=schedule.time_slot)
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

# Read all schedules (GET /schedules/)
@router.get("/", response_model=list[schemas.Schedule])
def get_schedules(db: Session = Depends(get_db)):
    schedules = db.query(models.Schedule).all()
    return schedules

# Read a single schedule by ID (GET /schedules/{schedule_id})
@router.get("/{schedule_id}", response_model=schemas.Schedule)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_schedule

# Update a schedule by ID (PUT /schedules/{schedule_id})
@router.put("/{schedule_id}", response_model=schemas.Schedule)
def update_schedule(schedule_id: int, schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    db_schedule.volunteer_id = schedule.volunteer_id
    db_schedule.event_id = schedule.event_id
    db_schedule.time_slot = schedule.time_slot
    
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

# Delete a schedule by ID (DELETE /schedules/{schedule_id})
@router.delete("/{schedule_id}", response_model=schemas.Schedule)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    db.delete(db_schedule)
    db.commit()
    return db_schedule
