from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey(
            "resumes.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
        index=True,
    )

    raw_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    skills: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    education: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    projects: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    experience: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    certifications: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    achievements: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    technologies: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    parser_version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    resume = relationship(
        "Resume",
        back_populates="analysis",
    )