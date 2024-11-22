from pydantic import BaseModel, EmailStr

class VolunteerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None

class VolunteerCreate(VolunteerBase):
    pass

class Volunteer(VolunteerBase):
    id: int

    class Config:
        orm_mode = True
