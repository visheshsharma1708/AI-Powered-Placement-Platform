from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.user import User


ALLOWED_EXTENSIONS = {".pdf", ".docx"}

MAX_FILE_SIZE = 5 * 1024 * 1024

RESUME_STORAGE_DIR = Path("backend/storage/resumes")


def validate_resume_file(file: UploadFile) -> str:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A file is required.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are supported.",
        )

    return extension


def get_next_version(
    db: Session,
    user_id: int,
) -> int:
    statement = (
        select(Resume.version)
        .where(Resume.user_id == user_id)
        .order_by(Resume.version.desc())
    )

    latest_version = db.execute(statement).scalars().first()

    if latest_version is None:
        return 1

    return latest_version + 1


async def save_resume(
    db: Session,
    user: User,
    file: UploadFile,
) -> Resume:
    extension = validate_resume_file(file)

    file_content = await file.read()

    if not file_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty.",
        )

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume file size must be 5 MB or less.",
        )

    RESUME_STORAGE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    version = get_next_version(
        db=db,
        user_id=user.id,
    )

    unique_name = (
        f"user_{user.id}_resume_{version}_{uuid4().hex}"
        f"{extension}"
    )

    file_path = RESUME_STORAGE_DIR / unique_name

    file_path.write_bytes(file_content)

    resume = Resume(
        user_id=user.id,
        file_name=file.filename,
        stored_file_name=unique_name,
        file_path=str(file_path),
        file_type=extension.replace(".", ""),
        file_size=len(file_content),
        version=version,
        is_active=True,
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


def get_user_resumes(
    db: Session,
    user_id: int,
) -> list[Resume]:
    statement = (
        select(Resume)
        .where(Resume.user_id == user_id)
        .order_by(Resume.version.desc())
    )

    return list(
        db.execute(statement).scalars().all()
    )


def get_resume(
    db: Session,
    user_id: int,
    resume_id: int,
) -> Resume:
    statement = (
        select(Resume)
        .where(
            Resume.id == resume_id,
            Resume.user_id == user_id,
        )
    )

    resume = db.execute(statement).scalars().first()

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    return resume


def delete_resume(
    db: Session,
    user_id: int,
    resume_id: int,
) -> None:
    resume = get_resume(
        db=db,
        user_id=user_id,
        resume_id=resume_id,
    )

    file_path = Path(resume.file_path)

    if file_path.exists():
        file_path.unlink()

    db.delete(resume)
    db.commit()