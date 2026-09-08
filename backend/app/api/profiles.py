from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.profile import (
    StudentProfileCreate,
    StudentProfileResponse,
    StudentProfileUpdate,
)
from app.services.profile_service import (
    create_profile,
    get_profile_by_user_id,
    update_profile,
)


router = APIRouter(
    prefix="/profiles",
    tags=["Student Profile"],
)


@router.get(
    "/me",
    response_model=StudentProfileResponse,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = get_profile_by_user_id(
        db,
        current_user.id,
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found.",
        )

    return profile


@router.post(
    "/me",
    response_model=StudentProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_my_profile(
    profile_data: StudentProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing_profile = get_profile_by_user_id(
        db,
        current_user.id,
    )

    if existing_profile is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student profile already exists.",
        )

    profile = create_profile(
        db=db,
        user_id=current_user.id,
        profile_data=profile_data.model_dump(
            mode="json",
            exclude_unset=True,
        ),
    )

    return profile


@router.put(
    "/me",
    response_model=StudentProfileResponse,
)
def update_my_profile(
    profile_data: StudentProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = get_profile_by_user_id(
        db,
        current_user.id,
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found.",
        )

    profile = update_profile(
        db=db,
        profile=profile,
        profile_data=profile_data.model_dump(
            mode="json",
            exclude_unset=True,
        ),
    )

    return profile