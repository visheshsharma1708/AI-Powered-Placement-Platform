from typing import Any


def generate_readiness_explanation(
    features: dict[str, float],
) -> dict[str, list[str]]:
    strengths: list[str] = []
    improvements: list[str] = []

    if features.get("skill_count", 0) >= 8:
        strengths.append(
            "A strong number of skills were identified in the resume."
        )
    else:
        improvements.append(
            "Add more relevant technical and role-specific skills."
        )

    if features.get("project_count", 0) >= 2:
        strengths.append(
            "The resume contains multiple projects."
        )
    else:
        improvements.append(
            "Add more practical projects with measurable outcomes."
        )

    if features.get("experience_count", 0) >= 1:
        strengths.append(
            "Relevant experience or internship information was detected."
        )
    else:
        improvements.append(
            "Consider adding internship, practical, or relevant experience."
        )

    if features.get("certification_count", 0) >= 1:
        strengths.append(
            "Relevant certification information was detected."
        )
    else:
        improvements.append(
            "Consider adding relevant certifications where appropriate."
        )

    if features.get("has_github", 0) == 1:
        strengths.append(
            "A GitHub profile is available."
        )
    else:
        improvements.append(
            "Add a GitHub profile containing relevant projects."
        )

    if features.get("has_linkedin", 0) == 1:
        strengths.append(
            "A LinkedIn profile is available."
        )
    else:
        improvements.append(
            "Add a professional LinkedIn profile."
        )

    if features.get("has_portfolio", 0) == 1:
        strengths.append(
            "A portfolio link is available."
        )
    else:
        improvements.append(
            "Consider adding a portfolio demonstrating practical work."
        )

    return {
        "strengths": strengths,
        "improvements": improvements,
    }
