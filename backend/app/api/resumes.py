from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.resume_analysis import ResumeAnalysis
from app.models.user import User
from app.schemas.resume import ResumeResponse
from app.schemas.resume_analysis import ResumeAnalysisResponse
from app.services.resume_analysis_service import (
    ResumeAnalysisError,
    analyze_and_save_resume,
)
from app.services.resume_extractor import (
    ResumeExtractionError,
    extract_resume_text,
)
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


@router.post(
    "/{resume_id}/extract",
)
def extract_resume(
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

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume file was not found in storage.",
        )

    try:
        extracted_text = extract_resume_text(
            str(file_path)
        )
    except ResumeExtractionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name,
        "character_count": len(extracted_text),
        "text": extracted_text,
    }


@router.post(
    "/{resume_id}/analyze",
    response_model=ResumeAnalysisResponse,
)
def analyze_resume_endpoint(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = get_resume(
        db=db,
        user_id=current_user.id,
        resume_id=resume_id,
    )

    try:
        return analyze_and_save_resume(
            db=db,
            resume=resume,
        )
    except ResumeAnalysisError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/{resume_id}/analysis",
    response_model=ResumeAnalysisResponse,
)
def get_resume_analysis(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = get_resume(
        db=db,
        user_id=current_user.id,
        resume_id=resume_id,
    )

    analysis = (
        db.query(ResumeAnalysis)
        .filter(
            ResumeAnalysis.resume_id == resume.id
        )
        .first()
    )

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Resume analysis not found. "
                "Analyze the resume first."
            ),
        )

    return analysis


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

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume file was not found in storage.",
        )

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