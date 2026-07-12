"""
Raw data loading utilities for the Inside Airbnb Market Intelligence project.

This module checks the expected raw data files and loads CSV-based datasets
into pandas DataFrames.

It is designed to make the project more reproducible outside notebooks.
"""

from pathlib import Path
from typing import Dict

import pandas as pd

from src.config import RAW_FILES


def check_raw_files() -> pd.DataFrame:
    """
    Check whether all expected raw data files exist.

    Returns:
        pd.DataFrame: File inventory with file name, path, existence status, and size.
    """
    inventory_rows = []

    for dataset_name, file_path in RAW_FILES.items():
        file_path = Path(file_path)

        inventory_rows.append(
            {
                "dataset_name": dataset_name,
                "file_name": file_path.name,
                "file_path": str(file_path),
                "file_exists": file_path.exists(),
                "file_size_mb": round(file_path.stat().st_size / (1024 * 1024), 2)
                if file_path.exists()
                else 0,
            }
        )

    return pd.DataFrame(inventory_rows)


def validate_raw_files_available() -> None:
    """
    Raise an error if any expected raw files are missing.

    This is useful before running a pipeline step that depends on raw data.
    """
    inventory_df = check_raw_files()

    missing_files = inventory_df[inventory_df["file_exists"] == False]

    if not missing_files.empty:
        missing_names = missing_files["file_name"].tolist()
        raise FileNotFoundError(
            f"Missing raw files: {missing_names}. "
            "Please download the required Inside Airbnb files first."
        )


def load_csv_dataset(dataset_name: str) -> pd.DataFrame:
    """
    Load one CSV or CSV.GZ dataset by dataset name.

    Args:
        dataset_name: Key from RAW_FILES dictionary.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    if dataset_name not in RAW_FILES:
        available_names = list(RAW_FILES.keys())
        raise ValueError(
            f"Unknown dataset name: {dataset_name}. "
            f"Available datasets: {available_names}"
        )

    file_path = RAW_FILES[dataset_name]

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix == ".geojson":
        raise ValueError(
            "GeoJSON files should be loaded using a geospatial library or JSON reader, "
            "not load_csv_dataset()."
        )

    return pd.read_csv(file_path)


def load_all_tabular_raw_datasets() -> Dict[str, pd.DataFrame]:
    """
    Load all raw CSV and CSV.GZ datasets.

    GeoJSON is intentionally excluded because it is not a normal CSV table.

    Returns:
        Dict[str, pd.DataFrame]: Dictionary of dataset name to DataFrame.
    """
    validate_raw_files_available()

    loaded_datasets = {}

    for dataset_name, file_path in RAW_FILES.items():
        if Path(file_path).suffix == ".geojson":
            continue

        loaded_datasets[dataset_name] = load_csv_dataset(dataset_name)

    return loaded_datasets


def summarize_loaded_datasets(datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Summarize loaded datasets with row and column counts.

    Args:
        datasets: Dictionary of loaded DataFrames.

    Returns:
        pd.DataFrame: Dataset shape summary.
    """
    summary_rows = []

    for dataset_name, dataframe in datasets.items():
        summary_rows.append(
            {
                "dataset_name": dataset_name,
                "row_count": dataframe.shape[0],
                "column_count": dataframe.shape[1],
            }
        )

    return pd.DataFrame(summary_rows)


if __name__ == "__main__":
    print("Checking raw data files...")
    print("-" * 60)

    inventory = check_raw_files()
    print(inventory)

    print("\nLoading tabular raw datasets...")
    print("-" * 60)

    datasets = load_all_tabular_raw_datasets()
    dataset_summary = summarize_loaded_datasets(datasets)

    print(dataset_summary)

    print("\nRaw data loading check completed successfully.")