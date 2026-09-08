from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ReadinessPrediction(Base):
    __tablename__ = "readiness_predictions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    readiness_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    readiness_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    prediction: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    features: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
    )

    explanation: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
    )

    model_version: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="logistic_regression_v1",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    user = relationship("User")
    resume = relationship("Resume")