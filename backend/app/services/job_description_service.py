from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job_description import JobDescription
from app.models.user import User
from app.schemas.job_description import JobDescriptionCreate, JobDescriptionUpdate


def create_job_description(
    db: Session,
    user: User,
    data: JobDescriptionCreate,
) -> JobDescription:

    job_description = JobDescription(
        user_id=user.id,
        title=data.title.strip(),
        company_name=(
            data.company_name.strip()
            if data.company_name
            else None
        ),
        description=data.description.strip(),
        source=(
            data.source.strip()
            if data.source
            else "manual"
        ),
    )

    db.add(job_description)
    db.commit()
    db.refresh(job_description)

    return job_description


def get_user_job_descriptions(
    db: Session,
    user_id: int,
) -> list[JobDescription]:

    statement = (
        select(JobDescription)
        .where(
            JobDescription.user_id == user_id
        )
        .order_by(
            JobDescription.created_at.desc()
        )
    )

    return list(
        db.execute(statement).scalars().all()
    )


def get_job_description(
    db: Session,
    user_id: int,
    job_description_id: int,
) -> JobDescription:

    statement = (
        select(JobDescription)
        .where(
            JobDescription.id == job_description_id,
            JobDescription.user_id == user_id,
        )
    )

    job_description = (
        db.execute(statement)
        .scalars()
        .first()
    )

    if job_description is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found.",
        )

    return job_description


def update_job_description(
    db: Session,
    user_id: int,
    job_description_id: int,
    data: JobDescriptionUpdate,
) -> JobDescription:

    job_description = get_job_description(
        db=db,
        user_id=user_id,
        job_description_id=job_description_id,
    )

    update_data = data.model_dump(
        exclude_unset=True
    )

    if "title" in update_data:
        job_description.title = (
            update_data["title"].strip()
        )

    if "company_name" in update_data:
        company_name = update_data["company_name"]

        job_description.company_name = (
            company_name.strip()
            if company_name
            else None
        )

    if "description" in update_data:
        job_description.description = (
            update_data["description"].strip()
        )

    if "source" in update_data:
        source = update_data["source"]

        job_description.source = (
            source.strip()
            if source
            else None
        )

    db.commit()
    db.refresh(job_description)

    return job_description


def delete_job_description(
    db: Session,
    user_id: int,
    job_description_id: int,
) -> None:

    job_description = get_job_description(
        db=db,
        user_id=user_id,
        job_description_id=job_description_id,
    )

    db.delete(job_description)
    db.commit()