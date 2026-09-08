from typing import Any


def _safe_count(value: Any) -> int:
    """
    Return the number of items in a list-like value.
    """

    if value is None:
        return 0

    if isinstance(value, list):
        return len(value)

    return 0


def build_readiness_features(
    analysis: Any,
    profile: Any | None = None,
) -> dict[str, float]:
    """
    Convert resume analysis and student profile information
    into numerical features for the readiness model.
    """

    features: dict[str, float] = {}

    features["skill_count"] = float(
        _safe_count(analysis.skills)
    )

    features["technology_count"] = float(
        _safe_count(analysis.technologies)
    )

    features["project_count"] = float(
        _safe_count(analysis.projects)
    )

    features["experience_count"] = float(
        _safe_count(analysis.experience)
    )

    features["certification_count"] = float(
        _safe_count(analysis.certifications)
    )

    features["achievement_count"] = float(
        _safe_count(analysis.achievements)
    )

    features["education_count"] = float(
        _safe_count(analysis.education)
    )

    features["resume_length"] = float(
        len(analysis.raw_text or "")
    )

    if profile is not None:
        features["has_github"] = float(
            bool(profile.github_url)
        )

        features["has_linkedin"] = float(
            bool(profile.linkedin_url)
        )

        features["has_portfolio"] = float(
            bool(profile.portfolio_url)
        )
    else:
        features["has_github"] = 0.0
        features["has_linkedin"] = 0.0
        features["has_portfolio"] = 0.0

    return features