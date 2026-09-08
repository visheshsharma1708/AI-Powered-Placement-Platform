from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ReadinessPredictionResponse(BaseModel):
    id: int
    resume_id: int
    readiness_probability: float
    readiness_score: float
    prediction: int
    features: dict[str, Any]
    explanation: dict[str, Any]
    model_version: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )