"""Clean and feature-engineer the raw healthcare tables for analytics.

The script is intentionally small enough to explain in an interview and explicit
enough to show the full Pandas workflow: load, validate, standardize, enrich,
and export an analysis-ready table.
"""

from pathlib import Path

import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def clean_admissions(admissions: pd.DataFrame, patients: pd.DataFrame) -> pd.DataFrame:
    frame = admissions.copy()
    frame.columns = frame.columns.str.strip().str.lower()
    frame["admission_date"] = pd.to_datetime(frame["admission_date"], errors="coerce")
    frame["discharge_date"] = pd.to_datetime(frame["discharge_date"], errors="coerce")

    frame = frame.drop_duplicates(subset=["admission_id"])
    frame = frame.dropna(subset=["admission_id", "patient_id", "admission_date"])
    frame = frame.loc[frame["discharge_date"] >= frame["admission_date"]]
    frame["length_of_stay"] = (
        frame["discharge_date"] - frame["admission_date"]
    ).dt.days.clip(lower=0)
    frame["readmission_flag"] = frame["readmitted"].astype("int8")

    frame = frame.merge(
        patients[["patient_id", "date_of_birth"]],
        on="patient_id",
        how="left",
        validate="many_to_one",
    )
    frame["date_of_birth"] = pd.to_datetime(frame["date_of_birth"], errors="coerce")
    frame["age"] = (
        (frame["admission_date"] - frame["date_of_birth"]).dt.days / 365.25
    ).round(1)
    frame["age_group"] = pd.cut(
        frame["age"],
        bins=[0, 35, 55, 75, float("inf")],
        labels=["Under 35", "35-54", "55-74", "75+"],
        right=False,
    ).astype("string")
    frame["length_of_stay_band"] = pd.cut(
        frame["length_of_stay"],
        bins=[-1, 2, 5, 10, float("inf")],
        labels=["0-2 days", "3-5 days", "6-10 days", "11+ days"],
    ).astype("string")
    frame["previous_admission_band"] = pd.cut(
        frame["previous_admissions"],
        bins=[-1, 0, 2, float("inf")],
        labels=["None", "1-2", "3+"],
    ).astype("string")
    return frame


def build_analysis_dataset() -> pd.DataFrame:
    admissions = pd.read_csv(RAW_DIR / "admissions.csv")
    patients = pd.read_csv(RAW_DIR / "patients.csv")
    billing = pd.read_csv(RAW_DIR / "billing.csv")
    treatments = pd.read_csv(RAW_DIR / "treatments.csv")

    clean = clean_admissions(admissions, patients)
    clean = clean.merge(
        treatments[["admission_id", "treatment_cost"]],
        on="admission_id",
        how="left",
        validate="one_to_one",
    )
    clean = clean.merge(
        billing[["admission_id", "insurance_coverage", "out_of_pocket_cost"]],
        on="admission_id",
        how="left",
        validate="one_to_one",
    )
    clean["treatment_cost"] = pd.to_numeric(clean["treatment_cost"], errors="coerce")
    clean["insurance_coverage"] = pd.to_numeric(
        clean["insurance_coverage"], errors="coerce"
    )
    clean["out_of_pocket_cost"] = pd.to_numeric(
        clean["out_of_pocket_cost"], errors="coerce"
    )
    return clean


if __name__ == "__main__":
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    analysis_ready = build_analysis_dataset()
    analysis_ready.to_csv(PROCESSED_DIR / "healthcare_analysis_ready.csv", index=False)
    print(f"Wrote {len(analysis_ready):,} analysis-ready admissions")