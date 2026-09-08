from pathlib import Path

from docx import Document
from pypdf import PdfReader


class ResumeExtractionError(Exception):
    """Raised when resume text extraction fails."""


def extract_text_from_pdf(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages).strip()

    except Exception as exc:
        raise ResumeExtractionError(
            f"Failed to extract text from PDF: {exc}"
        ) from exc


def extract_text_from_docx(file_path: str) -> str:
    try:
        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n".join(paragraphs).strip()

    except Exception as exc:
        raise ResumeExtractionError(
            f"Failed to extract text from DOCX: {exc}"
        ) from exc


def extract_resume_text(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise ResumeExtractionError("Resume file does not exist.")

    extension = path.suffix.lower()

    if extension == ".pdf":
        text = extract_text_from_pdf(str(path))

    elif extension == ".docx":
        text = extract_text_from_docx(str(path))

    else:
        raise ResumeExtractionError(
            "Unsupported resume format. Only PDF and DOCX are supported."
        )

    if not text:
        raise ResumeExtractionError(
            "No readable text was found in the resume."
        )

    return text