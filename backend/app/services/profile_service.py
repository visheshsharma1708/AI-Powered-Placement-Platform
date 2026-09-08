from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.student_profile import StudentProfile


def get_profile_by_user_id(
    db: Session,
    user_id: int,
) -> StudentProfile | None:

    statement = select(StudentProfile).where(
        StudentProfile.user_id == user_id
    )

    return db.scalar(statement)


def create_profile(
    db: Session,
    user_id: int,
    profile_data: dict,
) -> StudentProfile:

    profile = StudentProfile(
        user_id=user_id,
        **profile_data,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


def update_profile(
    db: Session,
    profile: StudentProfile,
    profile_data: dict,
) -> StudentProfile:

    for field, value in profile_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile