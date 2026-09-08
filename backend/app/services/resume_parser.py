import re
from typing import Any


SKILL_KEYWORDS = {
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "typescript",
    "sql",
    "html",
    "css",
    "react",
    "node.js",
    "fastapi",
    "django",
    "flask",
    "spring",
    "postgresql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "nlp",
    "data science",
    "data analysis",
    "rest api",
    "linux",
}


SECTION_ALIASES = {
    "skills": {
        "skills",
        "technical skills",
        "technical skill",
        "key skills",
        "core skills",
    },
    "education": {
        "education",
        "academic background",
        "academic qualifications",
        "qualifications",
    },
    "projects": {
        "projects",
        "academic projects",
        "personal projects",
        "key projects",
    },
    "experience": {
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships",
    },
    "certifications": {
        "certifications",
        "certificates",
        "licenses & certifications",
    },
    "achievements": {
        "achievements",
        "accomplishments",
        "awards",
        "honors",
    },
}


def clean_text(text: str) -> str:
    """Normalize extracted resume text."""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def normalize_heading(line: str) -> str:
    """Normalize a possible resume section heading."""

    line = line.strip().lower()
    line = re.sub(r"[:\-]+$", "", line)
    line = re.sub(r"\s+", " ", line)

    return line


def detect_sections(text: str) -> dict[str, str]:
    """Split resume text into common resume sections."""

    lines = text.splitlines()

    sections: dict[str, list[str]] = {}
    current_section: str | None = None

    for line in lines:
        normalized = normalize_heading(line)

        detected_section = None

        for section_name, aliases in SECTION_ALIASES.items():
            if normalized in aliases:
                detected_section = section_name
                break

        if detected_section:
            current_section = detected_section
            sections.setdefault(current_section, [])
            continue

        if current_section:
            sections[current_section].append(line)

    return {
        section_name: "\n".join(section_lines).strip()
        for section_name, section_lines in sections.items()
    }


def extract_skills(text: str) -> list[str]:
    """Extract known technical skills from resume text."""

    normalized_text = text.lower()

    found_skills = []

    for skill in sorted(SKILL_KEYWORDS, key=len, reverse=True):
        pattern = rf"(?<![a-zA-Z0-9+#.]){re.escape(skill)}(?![a-zA-Z0-9+#.])"

        if re.search(pattern, normalized_text):
            found_skills.append(skill)

    return sorted(set(found_skills))


def extract_list_items(section_text: str) -> list[str]:
    """Convert section text into clean list items."""

    if not section_text:
        return []

    lines = section_text.splitlines()

    items = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        line = re.sub(r"^[•●▪◦\-*]+\s*", "", line)
        line = line.strip()

        if line:
            items.append(line)

    return items


def extract_education(section_text: str) -> list[str]:
    """Extract education entries."""

    return extract_list_items(section_text)


def extract_projects(section_text: str) -> list[str]:
    """Extract project entries."""

    return extract_list_items(section_text)


def extract_experience(section_text: str) -> list[str]:
    """Extract experience entries."""

    return extract_list_items(section_text)


def extract_certifications(section_text: str) -> list[str]:
    """Extract certification entries."""

    return extract_list_items(section_text)


def extract_achievements(section_text: str) -> list[str]:
    """Extract achievement entries."""

    return extract_list_items(section_text)


def extract_technologies(text: str) -> list[str]:
    """Extract technology-related skills."""

    technology_terms = {
        "python",
        "java",
        "c",
        "c++",
        "javascript",
        "typescript",
        "react",
        "node.js",
        "fastapi",
        "django",
        "flask",
        "spring",
        "postgresql",
        "mysql",
        "mongodb",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "pandas",
        "numpy",
        "git",
        "github",
        "linux",
    }

    normalized_text = text.lower()

    technologies = []

    for technology in sorted(
        technology_terms,
        key=len,
        reverse=True,
    ):
        pattern = rf"(?<![a-zA-Z0-9+#.]){re.escape(technology)}(?![a-zA-Z0-9+#.])"

        if re.search(pattern, normalized_text):
            technologies.append(technology)

    return sorted(set(technologies))


def analyze_resume(text: str) -> dict[str, Any]:
    """Convert raw resume text into structured resume information."""

    cleaned_text = clean_text(text)

    sections = detect_sections(cleaned_text)

    skills = extract_skills(cleaned_text)

    education = extract_education(
        sections.get("education", "")
    )

    projects = extract_projects(
        sections.get("projects", "")
    )

    experience = extract_experience(
        sections.get("experience", "")
    )

    certifications = extract_certifications(
        sections.get("certifications", "")
    )

    achievements = extract_achievements(
        sections.get("achievements", "")
    )

    technologies = extract_technologies(cleaned_text)

    return {
        "raw_text": cleaned_text,
        "skills": skills,
        "education": education,
        "projects": projects,
        "experience": experience,
        "certifications": certifications,
        "achievements": achievements,
        "technologies": technologies,
    }