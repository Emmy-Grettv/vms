from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Volunteer
from schemas import Volunteer as VolunteerSchema, VolunteerCreate as VolunteerCreateSchema
from database import get_db

router = APIRouter()

# Create a Volunteer
@router.post("/volunteers/", response_model=VolunteerSchema)
def create_volunteer(volunteer: VolunteerCreateSchema, db: Session = Depends(get_db)):
    db_volunteer = db.query(Volunteer).filter(Volunteer.email == volunteer.email).first()
    if db_volunteer:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_volunteer = Volunteer(
        name=volunteer.name, 
        email=volunteer.email, 
        phone_number=volunteer.phone_number, 
        age=volunteer.age, 
        skills=volunteer.skills
    )
    db.add(db_volunteer)
    db.commit()
    db.refresh(db_volunteer)
    return db_volunteer

# Read All Volunteers
@router.get("/volunteers/", response_model=list[VolunteerSchema])
def get_volunteers(db: Session = Depends(get_db)):
    return db.query(Volunteer).all()

# Read Specific Volunteer by ID
@router.get("/volunteers/{volunteer_id}", response_model=VolunteerSchema)
def get_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    db_volunteer = db.query(Volunteer).filter(Volunteer.volunteer_id == volunteer_id).first()
    if db_volunteer is None:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    return db_volunteer

# Update a Volunteer
@router.put("/volunteers/{volunteer_id}", response_model=VolunteerSchema)
def update_volunteer(volunteer_id: int, volunteer: VolunteerCreateSchema, db: Session = Depends(get_db)):
    db_volunteer = db.query(Volunteer).filter(Volunteer.volunteer_id == volunteer_id).first()
    if db_volunteer is None:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    db_volunteer.name = volunteer.name
    db_volunteer.email = volunteer.email
    db_volunteer.phone_number = volunteer.phone_number
    db_volunteer.age = volunteer.age
    db_volunteer.skills = volunteer.skills
    db.commit()
    db.refresh(db_volunteer)
    return db_volunteer

# Delete a Volunteer
@router.delete("/volunteers/{volunteer_id}", response_model=VolunteerSchema)
def delete_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    db_volunteer = db.query(Volunteer).filter(Volunteer.volunteer_id == volunteer_id).first()
    if db_volunteer is None:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    db.delete(db_volunteer)
    db.commit()
    return db_volunteer
