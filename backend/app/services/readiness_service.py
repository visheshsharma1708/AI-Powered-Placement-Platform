from sqlalchemy.orm import Session

from app.ml.prediction_service import (
    ReadinessPredictionError,
    predict_readiness,
)
from app.models.readiness_prediction import ReadinessPrediction
from app.models.resume import Resume
from app.models.student_profile import StudentProfile


def generate_and_save_prediction(
    db: Session,
    resume: Resume,
) -> ReadinessPrediction:

    if resume.analysis is None:
        raise ReadinessPredictionError(
            "Resume analysis must be completed before readiness prediction."
        )

    profile = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.user_id == resume.user_id
        )
        .first()
    )

    result = predict_readiness(
        analysis=resume.analysis,
        profile=profile,
    )

    prediction = ReadinessPrediction(
        user_id=resume.user_id,
        resume_id=resume.id,
        readiness_probability=result[
            "readiness_probability"
        ],
        readiness_score=result[
            "readiness_score"
        ],
        prediction=result["prediction"],
        features=result["features"],
        explanation=result["explanation"],
        model_version="logistic_regression_v1",
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction