from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.db.dependencies import get_db


router = APIRouter(
    prefix="/database",
    tags=["Database"],
)


@router.get("/health")
def database_health(
    db: Session = Depends(get_db),
):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "PostgreSQL",
            "connection": "successful",
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(error)}",
        )