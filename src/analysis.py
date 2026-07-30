from pathlib import Path
import logging

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "icu_patients.csv"
REPORTS_DIR = BASE_DIR / "reports"
IMAGES_DIR = BASE_DIR / "images"

REQUIRED_COLUMNS = {
    "patient_id",
    "age",
    "diagnosis",
    "length_of_stay_days",
    "mechanical_ventilation",
    "outcome",
    "readmission",
}


def configure_logging() -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )


def load_data(file_path: Path) -> pd.DataFrame:
    """Load the ICU dataset and validate its structure."""
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    dataframe = pd.read_csv(file_path)

    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    if dataframe.empty:
        raise ValueError("The dataset is empty.")

    return dataframe


def clean_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates and invalid records."""
    cleaned = dataframe.copy()

    cleaned = cleaned.drop_duplicates(subset="patient_id")
    cleaned = cleaned.dropna(subset=list(REQUIRED_COLUMNS))

    cleaned = cleaned[
        cleaned["age"].between(0, 120)
        & cleaned["length_of_stay_days"].between(0, 365)
    ]

    return cleaned


def calculate_kpis(dataframe: pd.DataFrame) -> dict[str, float]:
    """Calculate the main ICU performance indicators."""
    return {
        "total_patients": int(len(dataframe)),
        "average_age": round(dataframe["age"].mean(), 1),
        "average_length_of_stay": round(
            dataframe["length_of_stay_days"].mean(), 1
        ),
        "mortality_rate": round(
            dataframe["outcome"].eq("Death").mean() * 100, 1
        ),
        "mechanical_ventilation_rate": round(
            dataframe["mechanical_ventilation"].eq("Yes").mean() * 100, 1
        ),
        "readmission_rate": round(
            dataframe["readmission"].eq("Yes").mean() * 100, 1
        ),
    }


def save_kpi_report(kpis: dict[str, float]) -> None:
    """Save KPI results as a CSV file."""
    report = pd.DataFrame(
        [{"metric": key, "value": value} for key, value in kpis.items()]
    )
    report.to_csv(REPORTS_DIR / "kpi_summary.csv", index=False)


def save_diagnosis_report(dataframe: pd.DataFrame) -> None:
    """Create an aggregated report by diagnosis."""
    report = (
        dataframe.groupby("diagnosis")
        .agg(
            patients=("patient_id", "count"),
            average_age=("age", "mean"),
            average_length_of_stay=("length_of_stay_days", "mean"),
            deaths=("outcome", lambda series: series.eq("Death").sum()),
            ventilation_cases=(
                "mechanical_ventilation",
                lambda series: series.eq("Yes").sum(),
            ),
        )
        .round(1)
        .sort_values("patients", ascending=False)
    )

    report.to_csv(REPORTS_DIR / "diagnosis_summary.csv")


def create_diagnosis_chart(dataframe: pd.DataFrame) -> None:
    """Create a horizontal bar chart by diagnosis."""
    counts = dataframe["diagnosis"].value_counts().sort_values()

    plt.figure(figsize=(10, 6))
    counts.plot(kind="barh")
    plt.title("Patients by Diagnosis")
    plt.xlabel("Number of Patients")
    plt.ylabel("Diagnosis")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "patients_by_diagnosis.png", dpi=150)
    plt.close()


def create_outcome_chart(dataframe: pd.DataFrame) -> None:
    """Create a bar chart for patient outcomes."""
    counts = dataframe["outcome"].value_counts()

    plt.figure(figsize=(7, 5))
    counts.plot(kind="bar")
    plt.title("Patient Outcomes")
    plt.xlabel("Outcome")
    plt.ylabel("Number of Patients")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "patient_outcomes.png", dpi=150)
    plt.close()


def create_length_of_stay_chart(dataframe: pd.DataFrame) -> None:
    """Create a histogram for ICU length of stay."""
    plt.figure(figsize=(9, 5))
    plt.hist(dataframe["length_of_stay_days"], bins=14, edgecolor="black")
    plt.title("ICU Length of Stay Distribution")
    plt.xlabel("Length of Stay (Days)")
    plt.ylabel("Number of Patients")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "length_of_stay_distribution.png", dpi=150)
    plt.close()


def print_summary(kpis: dict[str, float]) -> None:
    """Print a readable summary in the terminal."""
    print("\nICU DATA ANALYSIS")
    print("=" * 45)
    print(f"Total patients: {kpis['total_patients']}")
    print(f"Average age: {kpis['average_age']}")
    print(
        "Average length of stay: "
        f"{kpis['average_length_of_stay']} days"
    )
    print(f"Mortality rate: {kpis['mortality_rate']}%")
    print(
        "Mechanical ventilation rate: "
        f"{kpis['mechanical_ventilation_rate']}%"
    )
    print(f"Readmission rate: {kpis['readmission_rate']}%")
    print("=" * 45)


def main() -> None:
    """Run the complete analysis workflow."""
    configure_logging()
    REPORTS_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(exist_ok=True)

    logging.info("Loading dataset.")
    dataframe = load_data(DATA_FILE)

    logging.info("Cleaning dataset.")
    dataframe = clean_data(dataframe)

    logging.info("Calculating KPIs.")
    kpis = calculate_kpis(dataframe)

    logging.info("Generating reports.")
    save_kpi_report(kpis)
    save_diagnosis_report(dataframe)

    logging.info("Generating charts.")
    create_diagnosis_chart(dataframe)
    create_outcome_chart(dataframe)
    create_length_of_stay_chart(dataframe)

    print_summary(kpis)
    logging.info("Analysis completed successfully.")


if __name__ == "__main__":
    try:
        main()
    except (
        FileNotFoundError,
        ValueError,
        pd.errors.ParserError,
    ) as error:
        logging.error(error)
