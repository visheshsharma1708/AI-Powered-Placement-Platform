from pathlib import Path

import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    BASE_DIR
    / "data"
    / "ml"
    / "readiness_training_data.csv"
)

MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "readiness_model.joblib"


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

TARGET_COLUMN = "readiness_label"


def load_dataset() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Training dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing dataset columns: {missing_columns}"
        )

    return df


def build_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> Pipeline:
    model = build_pipeline()

    model.fit(
        X_train,
        y_train,
    )

    return model


def evaluate_model(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> None:
    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0,
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities,
    )

    print("\n===== MODEL EVALUATION =====")

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")

    print("\n===== CONFUSION MATRIX =====")

    print(
        confusion_matrix(
            y_test,
            predictions,
        )
    )

    print("\n===== CLASSIFICATION REPORT =====")

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )


def save_model(model: Pipeline) -> None:
    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    print(
        f"\nModel saved to:\n{MODEL_PATH}"
    )


def main() -> None:
    print("===== READINESS MODEL TRAINING =====")

    df = load_dataset()

    print(
        f"Dataset loaded successfully: {len(df)} rows"
    )

    X = df[FEATURE_COLUMNS]

    y = df[TARGET_COLUMN]

    print(
        f"Features: {len(FEATURE_COLUMNS)}"
    )

    print(
        f"Target classes: {sorted(y.unique())}"
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    print(
        f"Training samples: {len(X_train)}"
    )

    print(
        f"Testing samples: {len(X_test)}"
    )

    model = train_model(
        X_train,
        y_train,
    )

    evaluate_model(
        model,
        X_test,
        y_test,
    )

    save_model(model)


if __name__ == "__main__":
    main()