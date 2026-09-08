from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.resume import ResumeResponse
from app.services.resume_service import (
    delete_resume,
    get_resume,
    get_user_resumes,
    save_resume,
)


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await save_resume(
        db=db,
        user=current_user,
        file=file,
    )


@router.get(
    "/",
    response_model=list[ResumeResponse],
)
def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_resumes(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{resume_id}/download",
)
def download_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = get_resume(
        db=db,
        user_id=current_user.id,
        resume_id=resume_id,
    )

    file_path = Path(resume.file_path)

    return FileResponse(
        path=file_path,
        filename=resume.file_name,
        media_type="application/octet-stream",
    )


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_resume(
        db=db,
        user_id=current_user.id,
        resume_id=resume_id,
    )