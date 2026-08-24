from fastapi import FastAPI


app = FastAPI(
    title="Placement Intelligence & Career Readiness Platform",
    description=(
        "AI, machine learning, NLP, and cloud-powered platform "
        "for resume intelligence and career readiness analysis."
    ),
    version="1.0.0",
)


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