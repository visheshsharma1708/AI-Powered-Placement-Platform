from pathlib import Path

from app.services.resume_extractor import extract_resume_text


BACKEND_DIRECTORY = Path(__file__).resolve().parent
RESUME_DIRECTORY = BACKEND_DIRECTORY / "storage" / "resumes"


def main() -> None:
    resume_files = list(RESUME_DIRECTORY.glob("*.pdf"))
    resume_files.extend(RESUME_DIRECTORY.glob("*.docx"))

    if not resume_files:
        print(f"No PDF or DOCX resume found in: {RESUME_DIRECTORY}")
        return

    for resume_path in resume_files:
        print(f"\nTesting resume: {resume_path}")
        print("=" * 60)

        try:
            text = extract_resume_text(str(resume_path))

            print(text)

            print("=" * 60)
            print("Resume extraction successful.")
            print(f"Characters extracted: {len(text)}")

        except Exception as exc:
            print("=" * 60)
            print(f"Resume extraction failed: {exc}")


if __name__ == "__main__":
    main()