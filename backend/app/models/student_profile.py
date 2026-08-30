from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    university: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    degree: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    branch: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    graduation_year: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    target_role: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    github_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    linkedin_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    portfolio_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    bio: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
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

    user = relationship(
        "User",
        back_populates="student_profile",
    )