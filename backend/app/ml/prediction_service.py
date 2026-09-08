from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from app.ml.feature_engineering import build_readiness_features


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "readiness_model.joblib"
)


FEATURE_COLUMNS = [
    "skill_count",
    "technology_count",
    "project_count",
    "experience_count",
    "certification_count",
    "achievement_count",
    "education_count",
    "resume_length",
    "has_github",
    "has_linkedin",
    "has_portfolio",
]


FEATURE_LABELS = {
    "skill_count": "Skills",
    "technology_count": "Technologies",
    "project_count": "Projects",
    "experience_count": "Experience",
    "certification_count": "Certifications",
    "achievement_count": "Achievements",
    "education_count": "Education",
    "resume_length": "Resume Content",
    "has_github": "GitHub Profile",
    "has_linkedin": "LinkedIn Profile",
    "has_portfolio": "Portfolio",
}


class ReadinessPredictionError(Exception):
    """Raised when readiness prediction fails."""


def load_readiness_model() -> Any:
    """
    Load the trained readiness model from disk.
    """

    if not MODEL_PATH.exists():
        raise ReadinessPredictionError(
            f"Readiness model not found: {MODEL_PATH}"
        )

    try:
        return joblib.load(MODEL_PATH)

    except Exception as exc:
        raise ReadinessPredictionError(
            "Unable to load the readiness model."
        ) from exc


def build_explanation(
    model: Any,
    feature_row: dict[str, float],
) -> dict[str, Any]:
    """
    Generate an explainable summary of the model prediction.

    The Logistic Regression coefficients are combined with
    the standardized feature values to estimate the contribution
    of each feature to the model's prediction.
    """

    try:
        if not hasattr(model, "named_steps"):
            raise ValueError(
                "The readiness model is not a supported pipeline."
            )

        classifier = model.named_steps.get("classifier")
        scaler = model.named_steps.get("scaler")

        if classifier is None:
            raise ValueError(
                "Classifier step not found in readiness model."
            )

        if scaler is None:
            raise ValueError(
                "Scaler step not found in readiness model."
            )

        if not hasattr(classifier, "coef_"):
            raise ValueError(
                "The classifier does not expose coefficients."
            )

        coefficients = classifier.coef_[0]

        feature_dataframe = pd.DataFrame(
            [feature_row],
            columns=FEATURE_COLUMNS,
        )

        scaled_features = scaler.transform(
            feature_dataframe
        )[0]

        contributions: list[dict[str, Any]] = []

        for index, feature_name in enumerate(
            FEATURE_COLUMNS
        ):
            contribution = float(
                coefficients[index]
                * scaled_features[index]
            )

            contributions.append(
                {
                    "feature": feature_name,
                    "label": FEATURE_LABELS.get(
                        feature_name,
                        feature_name,
                    ),
                    "value": feature_row[feature_name],
                    "contribution": round(
                        contribution,
                        4,
                    ),
                }
            )

        positive_factors = sorted(
            [
                item
                for item in contributions
                if item["contribution"] > 0
            ],
            key=lambda item: item["contribution"],
            reverse=True,
        )

        improvement_areas = sorted(
            [
                item
                for item in contributions
                if item["contribution"] < 0
            ],
            key=lambda item: item["contribution"],
        )

        return {
            "positive_factors": positive_factors[:5],
            "improvement_areas": improvement_areas[:5],
            "all_features": contributions,
        }

    except ReadinessPredictionError:
        raise

    except Exception as exc:
        raise ReadinessPredictionError(
            "Unable to generate prediction explanation."
        ) from exc


def predict_readiness(
    analysis: Any,
    profile: Any | None = None,
) -> dict[str, Any]:
    """
    Generate a career-readiness estimate using the
    trained machine-learning model.

    The returned score represents an estimated readiness
    level based on the available resume and profile data.
    It is not a guarantee of placement.
    """

    try:
        features = build_readiness_features(
            analysis=analysis,
            profile=profile,
        )

        feature_row = {
            column: float(
                features.get(
                    column,
                    0.0,
                )
            )
            for column in FEATURE_COLUMNS
        }

        input_data = pd.DataFrame(
            [feature_row],
            columns=FEATURE_COLUMNS,
        )

        model = load_readiness_model()

        prediction = int(
            model.predict(input_data)[0]
        )

        probabilities = model.predict_proba(
            input_data
        )[0]

        if len(probabilities) < 2:
            raise ReadinessPredictionError(
                "The readiness model does not provide "
                "binary classification probabilities."
            )

        probability = float(
            probabilities[1]
        )

        readiness_score = round(
            probability * 100,
            2,
        )

        explanation = build_explanation(
            model=model,
            feature_row=feature_row,
        )

        return {
            "prediction": prediction,
            "readiness_probability": round(
                probability,
                4,
            ),
            "readiness_score": readiness_score,
            "features": feature_row,
            "explanation": explanation,
        }

    except ReadinessPredictionError:
        raise

    except Exception as exc:
        raise ReadinessPredictionError(
            "Unable to generate readiness prediction."
        ) from exc