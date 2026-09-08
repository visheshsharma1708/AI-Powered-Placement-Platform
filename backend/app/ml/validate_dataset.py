from pathlib import Path

import pandas as pd


DATASET_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "ml"
    / "readiness_training_data.csv"
)


REQUIRED_COLUMNS = [
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
    "readiness_label",
]


def validate_dataset() -> None:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError("Dataset is empty.")

    if df.isnull().any().any():
        raise ValueError(
            "Dataset contains missing values."
        )

    labels = set(df["readiness_label"].unique())

    if not labels.issubset({0, 1}):
        raise ValueError(
            "readiness_label must contain only 0 and 1."
        )

    if df["readiness_label"].nunique() < 2:
        raise ValueError(
            "Dataset must contain both classes: 0 and 1."
        )

    print("===== DATASET VALIDATION =====")
    print(f"Dataset path: {DATASET_PATH}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print()
    print("Class distribution:")
    print(df["readiness_label"].value_counts())
    print()
    print("Dataset validation successful.")


if __name__ == "__main__":
    validate_dataset()