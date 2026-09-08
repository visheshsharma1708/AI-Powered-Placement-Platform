from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.dependencies import get_db
from app.ml.prediction_service import ReadinessPredictionError
from app.models.resume import Resume
from app.models.user import User
from app.schemas.readiness import ReadinessPredictionResponse
from app.services.readiness_service import (
    generate_and_save_prediction,
)


router = APIRouter(
    prefix="/readiness",
    tags=["Readiness"],
)


@router.post(
    "/{resume_id}/predict",
    response_model=ReadinessPredictionResponse,
)
def predict_resume_readiness(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id,
        )
        .first()
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    try:
        return generate_and_save_prediction(
            db=db,
            resume=resume,
        )

    except ReadinessPredictionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc