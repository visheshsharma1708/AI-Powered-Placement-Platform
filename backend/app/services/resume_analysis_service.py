from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.resume_analysis import ResumeAnalysis
from app.services.resume_extractor import (
    ResumeExtractionError,
    extract_resume_text,
)
from app.services.resume_parser import analyze_resume


class ResumeAnalysisError(Exception):
    """Raised when resume analysis cannot be completed."""


def analyze_and_save_resume(
    db: Session,
    resume: Resume,
) -> ResumeAnalysis:

    try:
        extracted_text = extract_resume_text(resume.file_path)
    except ResumeExtractionError as exc:
        raise ResumeAnalysisError(
            f"Unable to extract resume text: {exc}"
        ) from exc

    if not extracted_text.strip():
        raise ResumeAnalysisError(
            "The resume does not contain readable text."
        )

    parsed_data = analyze_resume(extracted_text)

    existing_analysis = (
        db.query(ResumeAnalysis)
        .filter(ResumeAnalysis.resume_id == resume.id)
        .first()
    )

    if existing_analysis:
        existing_analysis.raw_text = parsed_data["raw_text"]
        existing_analysis.skills = parsed_data["skills"]
        existing_analysis.education = parsed_data["education"]
        existing_analysis.projects = parsed_data["projects"]
        existing_analysis.experience = parsed_data["experience"]
        existing_analysis.certifications = parsed_data["certifications"]
        existing_analysis.achievements = parsed_data["achievements"]
        existing_analysis.technologies = parsed_data["technologies"]
        existing_analysis.parser_version = 1

        db.commit()
        db.refresh(existing_analysis)

        return existing_analysis

    analysis = ResumeAnalysis(
        resume_id=resume.id,
        raw_text=parsed_data["raw_text"],
        skills=parsed_data["skills"],
        education=parsed_data["education"],
        projects=parsed_data["projects"],
        experience=parsed_data["experience"],
        certifications=parsed_data["certifications"],
        achievements=parsed_data["achievements"],
        technologies=parsed_data["technologies"],
        parser_version=1,
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis