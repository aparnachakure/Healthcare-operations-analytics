"""Baseline readmission model for the healthcare analytics project.

This is a deliberately explainable baseline. It is not a clinical decision tool.
The goal is to demonstrate a clean train/evaluate workflow and identify which
operational features are associated with readmission risk.
"""

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


DATA_PATH = Path("data/processed/healthcare_analysis_ready.csv")


def train_baseline_model() -> None:
    data = pd.read_csv(DATA_PATH)
    target = "readmission_flag"
    features = [
        "age",
        "length_of_stay",
        "previous_admissions",
        "treatment_cost",
        "diagnosis",
        "admission_type",
        "age_group",
        "length_of_stay_band",
    ]
    x_train, x_test, y_train, y_test = train_test_split(
        data[features],
        data[target],
        test_size=0.25,
        random_state=42,
        stratify=data[target],
    )

    numeric_features = [
        "age",
        "length_of_stay",
        "previous_admissions",
        "treatment_cost",
    ]
    categorical_features = [
        "diagnosis",
        "admission_type",
        "age_group",
        "length_of_stay_band",
    ]

    preprocess = ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_features,
            ),
            (
                "categorical",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("one_hot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_features,
            ),
        ]
    )
    model = Pipeline(
        [
            ("preprocess", preprocess),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )
    model.fit(x_train, y_train)
    probability = model.predict_proba(x_test)[:, 1]
    prediction = (probability >= 0.5).astype(int)
    print(f"ROC-AUC: {roc_auc_score(y_test, probability):.3f}")
    print(classification_report(y_test, prediction, zero_division=0))


if __name__ == "__main__":
    train_baseline_model()