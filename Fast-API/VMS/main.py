from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from database import Base, engine
import models
from volunteers.routes import router as volunteer_router
from events.routes import router as events_router  
from participation.routes import router as participation_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(volunteer_router, prefix="/volunteers", tags=["volunteers"])
app.include_router(events_router, prefix="/events", tags=["events"])
app.include_router(participation_router, prefix="/participations", tags=["participation"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Volunteer Management System API!"}

# Exception handler for HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": "An error occurred",
            "detail": exc.detail,
        },
    )

# Exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation error",
            "errors": exc.errors(),
        },
    )
