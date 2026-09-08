from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.api import resumes
from app.api.profiles import router as profiles_router
from app.api.database import router as database_router


app = FastAPI(
    title="Placement Intelligence & Career Readiness Platform",
    description=(
        "AI, machine learning, NLP, and cloud-powered platform "
        "for resume intelligence and career readiness analysis."
    ),
    version="1.0.0",
)


app.include_router(database_router)
app.include_router(auth_router)
app.include_router(resumes.router)
app.include_router(users_router)
app.include_router(profiles_router)
@app.get("/", tags=["System"])
def root():
    return {
        "message": "Placement Intelligence Backend is running successfully",
        "documentation": "/docs",
        "health_check": "/health",
    }


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "placement-intelligence-backend",
        "version": "1.0.0",
    }