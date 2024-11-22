from fastapi import FastAPI
from volunteers.routes import router as volunteer_router
from events.routes import router as event_router
from schedules.routes import router as schedule_router
from database import Base, engine
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(volunteer_router, prefix="/volunteers", tags=["volunteers"])
app.include_router(event_router, prefix="/events", tags=["events"])
app.include_router(schedule_router, prefix="/schedules", tags=["schedules"])


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": "An error occurred",
            "detail": exc.detail,
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation error",
            "errors": exc.errors(),
        },
    )

