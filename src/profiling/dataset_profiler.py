"""
Dataset profiling utilities for the Inside Airbnb Market Intelligence project.

This module creates reusable dataset-level and column-level profiles for raw
or processed pandas DataFrames.
"""

from typing import Dict

import pandas as pd

from src.config import DATA_QUALITY_REPORTS_DIR
from src.ingestion.raw_data_loader import load_all_tabular_raw_datasets


def create_dataset_inventory(datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Create a dataset-level inventory showing row and column counts.

    Args:
        datasets: Dictionary of dataset names and DataFrames.

    Returns:
        pd.DataFrame: Dataset inventory summary.
    """
    inventory_rows = []

    for dataset_name, dataframe in datasets.items():
        inventory_rows.append(
            {
                "dataset_name": dataset_name,
                "row_count": dataframe.shape[0],
                "column_count": dataframe.shape[1],
                "duplicate_row_count": dataframe.duplicated().sum(),
            }
        )

    return pd.DataFrame(inventory_rows)


def create_schema_profile(datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Create a column-level schema profile for multiple datasets.

    Args:
        datasets: Dictionary of dataset names and DataFrames.

    Returns:
        pd.DataFrame: Schema profile with data type, missing values, unique values,
        and sample values.
    """
    profile_rows = []

    for dataset_name, dataframe in datasets.items():
        row_count = len(dataframe)

        for column in dataframe.columns:
            missing_count = dataframe[column].isna().sum()
            missing_percentage = (
                round((missing_count / row_count) * 100, 2)
                if row_count > 0
                else 0
            )

            sample_values = (
                dataframe[column]
                .dropna()
                .astype(str)
                .head(3)
                .tolist()
            )

            profile_rows.append(
                {
                    "dataset_name": dataset_name,
                    "column_name": column,
                    "data_type": str(dataframe[column].dtype),
                    "missing_count": missing_count,
                    "missing_percentage": missing_percentage,
                    "unique_count": dataframe[column].nunique(dropna=True),
                    "sample_values": " | ".join(sample_values),
                }
            )

    return pd.DataFrame(profile_rows)


def create_missing_value_summary(datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Create a missing value summary for all columns in all datasets.

    Args:
        datasets: Dictionary of dataset names and DataFrames.

    Returns:
        pd.DataFrame: Missing value summary.
    """
    missing_rows = []

    for dataset_name, dataframe in datasets.items():
        row_count = len(dataframe)

        for column in dataframe.columns:
            missing_count = dataframe[column].isna().sum()
            missing_percentage = (
                round((missing_count / row_count) * 100, 2)
                if row_count > 0
                else 0
            )

            missing_rows.append(
                {
                    "dataset_name": dataset_name,
                    "column_name": column,
                    "missing_count": missing_count,
                    "missing_percentage": missing_percentage,
                }
            )

    missing_summary = pd.DataFrame(missing_rows)

    return missing_summary.sort_values(
        ["missing_percentage", "missing_count"],
        ascending=False,
    )


def save_profile_outputs(
    dataset_inventory: pd.DataFrame,
    schema_profile: pd.DataFrame,
    missing_value_summary: pd.DataFrame,
) -> None:
    """
    Save profiling outputs to the data quality reports folder.

    Args:
        dataset_inventory: Dataset-level inventory DataFrame.
        schema_profile: Column-level schema profile DataFrame.
        missing_value_summary: Missing value summary DataFrame.
    """
    DATA_QUALITY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    dataset_inventory.to_csv(
        DATA_QUALITY_REPORTS_DIR / "dataset_inventory_from_src.csv",
        index=False,
    )

    schema_profile.to_csv(
        DATA_QUALITY_REPORTS_DIR / "schema_profile_from_src.csv",
        index=False,
    )

    missing_value_summary.to_csv(
        DATA_QUALITY_REPORTS_DIR / "missing_value_summary_from_src.csv",
        index=False,
    )


if __name__ == "__main__":
    print("Loading raw tabular datasets...")
    datasets = load_all_tabular_raw_datasets()

    print("Creating dataset inventory...")
    dataset_inventory = create_dataset_inventory(datasets)

    print("Creating schema profile...")
    schema_profile = create_schema_profile(datasets)

    print("Creating missing value summary...")
    missing_value_summary = create_missing_value_summary(datasets)

    print("Saving profiling outputs...")
    save_profile_outputs(
        dataset_inventory=dataset_inventory,
        schema_profile=schema_profile,
        missing_value_summary=missing_value_summary,
    )

    print("\nDataset inventory:")
    print(dataset_inventory)

    print("\nTop missing value rows:")
    print(missing_value_summary.head(15))

    print("\nDataset profiling completed successfully.")