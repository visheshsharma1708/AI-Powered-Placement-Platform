from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.job_description import (
    JobDescriptionCreate,
    JobDescriptionResponse,
    JobDescriptionUpdate,
)
from app.services.job_description_service import (
    create_job_description,
    delete_job_description,
    get_job_description,
    get_user_job_descriptions,
    update_job_description,
)


router = APIRouter(
    prefix="/job-descriptions",
    tags=["Job Descriptions"],
)


@router.post(
    "/",
    response_model=JobDescriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job_description_endpoint(
    data: JobDescriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_job_description(
        db=db,
        user=current_user,
        data=data,
    )


@router.get(
    "/",
    response_model=list[JobDescriptionResponse],
)
def list_job_descriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_job_descriptions(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{job_description_id}",
    response_model=JobDescriptionResponse,
)
def get_job_description_endpoint(
    job_description_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_job_description(
        db=db,
        user_id=current_user.id,
        job_description_id=job_description_id,
    )


@router.put(
    "/{job_description_id}",
    response_model=JobDescriptionResponse,
)
def update_job_description_endpoint(
    job_description_id: int,
    data: JobDescriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_job_description(
        db=db,
        user_id=current_user.id,
        job_description_id=job_description_id,
        data=data,
    )


@router.delete(
    "/{job_description_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_job_description_endpoint(
    job_description_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_job_description(
        db=db,
        user_id=current_user.id,
        job_description_id=job_description_id,
    )