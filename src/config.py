"""Project configuration and reusable file paths."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


CITY_NAME = "amsterdam"
SNAPSHOT_DATE = "2026-06-15"

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
RAW_CITY_DIR = RAW_DATA_DIR / CITY_NAME / SNAPSHOT_DATE

PROCESSED_DATA_DIR = DATA_DIR / "processed"
PROCESSED_CITY_DIR = PROCESSED_DATA_DIR / CITY_NAME

INTERIM_DATA_DIR = DATA_DIR / "interim"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

REPORTS_DIR = PROJECT_ROOT / "reports"
DATA_QUALITY_REPORTS_DIR = REPORTS_DIR / "data_quality"
ANALYTICS_OUTPUTS_DIR = REPORTS_DIR / "analytics_outputs"
STATISTICAL_ANALYSIS_DIR = REPORTS_DIR / "statistical_analysis"
MACHINE_LEARNING_REPORTS_DIR = REPORTS_DIR / "machine_learning"
FIGURES_DIR = REPORTS_DIR / "figures"
MODELS_DIR = PROJECT_ROOT / "models"
WAREHOUSE_DIR = PROJECT_ROOT / "warehouse"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
SQL_DIR = PROJECT_ROOT / "sql"
DDL_DIR = PROJECT_ROOT / "ddl"

DUCKDB_DATABASE_PATH = WAREHOUSE_DIR / "airbnb_market.duckdb"
FINAL_MODEL_PATH = MODELS_DIR / "random_forest_price_prediction_model.joblib"

RAW_FILES = {
    "detailed_listings": RAW_CITY_DIR / "listings.csv.gz",
    "calendar": RAW_CITY_DIR / "calendar.csv.gz",
    "detailed_reviews": RAW_CITY_DIR / "reviews.csv.gz",
    "summary_listings": RAW_CITY_DIR / "listings.csv",
    "summary_reviews": RAW_CITY_DIR / "reviews.csv",
    "neighbourhoods": RAW_CITY_DIR / "neighbourhoods.csv",
    "neighbourhoods_geojson": RAW_CITY_DIR / "neighbourhoods.geojson",
}


# ---------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------

def create_project_directories() -> None:
    """Create commonly used project directories if they do not already exist."""
    directories = [
        RAW_DATA_DIR,
        RAW_CITY_DIR,
        PROCESSED_DATA_DIR,
        PROCESSED_CITY_DIR,
        INTERIM_DATA_DIR,
        EXTERNAL_DATA_DIR,
        REPORTS_DIR,
        DATA_QUALITY_REPORTS_DIR,
        ANALYTICS_OUTPUTS_DIR,
        STATISTICAL_ANALYSIS_DIR,
        MACHINE_LEARNING_REPORTS_DIR,
        FIGURES_DIR,
        MODELS_DIR,
        WAREHOUSE_DIR,
        NOTEBOOKS_DIR,
        SQL_DIR,
        DDL_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def get_project_status() -> dict:
    """
    Return a simple project path status dictionary.
    Useful for quick checks in scripts and notebooks.
    """
    return {
        "project_root": str(PROJECT_ROOT),
        "raw_city_dir_exists": RAW_CITY_DIR.exists(),
        "processed_city_dir_exists": PROCESSED_CITY_DIR.exists(),
        "warehouse_exists": DUCKDB_DATABASE_PATH.exists(),
        "model_exists": FINAL_MODEL_PATH.exists(),
        "reports_dir_exists": REPORTS_DIR.exists(),
    }


if __name__ == "__main__":
    create_project_directories()

    status = get_project_status()

    print("Project configuration loaded successfully.")
    print("-" * 60)

    for key, value in status.items():
        print(f"{key}: {value}")