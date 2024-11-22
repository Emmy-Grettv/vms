from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from volunteers import schemas, models
from typing import List
from pydantic import EmailStr, ValidationError
import logging
from pydantic import ValidationError

router = APIRouter()

# Response model for consistent message and data structure
class VolunteerResponse(schemas.BaseModel):
    message: str
    volunteer: schemas.Volunteer

class VolunteersResponse(schemas.BaseModel):
    message: str
    volunteers: List[schemas.Volunteer]

# Create a new volunteer
@router.post("/", response_model=VolunteerResponse)
def create_volunteer(volunteer: schemas.VolunteerCreate, db: Session = Depends(get_db)):
    db_volunteer = models.Volunteer(name=volunteer.name, email=volunteer.email, phone=volunteer.phone)
    db.add(db_volunteer)
    db.commit()
    db.refresh(db_volunteer)

    serialized_volunteer = schemas.Volunteer(
        id=db_volunteer.id, name=db_volunteer.name, email=db_volunteer.email, phone=db_volunteer.phone
    )
    return {"message": "Volunteer created successfully", "volunteer": serialized_volunteer}

# Read all volunteers
logging.basicConfig(level=logging.INFO)

@router.get("/", response_model=VolunteersResponse)
async def read_volunteers(db: Session = Depends(get_db)):
    db_volunteers = db.query(models.Volunteer).all()
    valid_volunteers = []
    for v in db_volunteers:
        try:
            # Validate and append valid volunteers
            valid_volunteers.append(
                schemas.Volunteer(id=v.id, name=v.name, email=v.email, phone=v.phone)
            )
        except ValidationError as e:
            # Log the invalid email
            logging.error(f"Skipping invalid volunteer with ID {v.id}: {v.email}")
            
    return {"message": "Volunteers retrieved successfully", "volunteers": valid_volunteers}

# Read a single volunteer by ID
@router.get("/{volunteer_id}", response_model=VolunteerResponse)
def read_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    db_volunteer = db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()
    if not db_volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")

    serialized_volunteer = schemas.Volunteer(
        id=db_volunteer.id, name=db_volunteer.name, email=db_volunteer.email, phone=db_volunteer.phone
    )
    return {"message": "Volunteer retrieved successfully", "volunteer": serialized_volunteer}

# Update an existing volunteer by ID
@router.put("/{volunteer_id}", response_model=VolunteerResponse)
def update_volunteer(volunteer_id: int, volunteer: schemas.VolunteerCreate, db: Session = Depends(get_db)):
    db_volunteer = db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()
    if not db_volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")

    db_volunteer.name = volunteer.name
    db_volunteer.email = volunteer.email
    db_volunteer.phone = volunteer.phone
    db.commit()
    db.refresh(db_volunteer)

    serialized_volunteer = schemas.Volunteer(
        id=db_volunteer.id, name=db_volunteer.name, email=db_volunteer.email, phone=db_volunteer.phone
    )
    return {"message": "Volunteer updated successfully", "volunteer": serialized_volunteer}

# Delete a volunteer by ID
@router.delete("/{volunteer_id}", response_model=VolunteerResponse)
def delete_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    db_volunteer = db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()
    if not db_volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")

    serialized_volunteer = schemas.Volunteer(
        id=db_volunteer.id, name=db_volunteer.name, email=db_volunteer.email, phone=db_volunteer.phone
    )

    db.delete(db_volunteer)
    db.commit()
    return {"message": "Volunteer deleted successfully", "volunteer": serialized_volunteer}
