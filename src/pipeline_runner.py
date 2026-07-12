"""
End-to-end pipeline runner for the Inside Airbnb Market Intelligence project.

This script runs the main reusable pipeline stages in order:

1. Create project directories
2. Check raw data files
3. Generate raw dataset profiling reports
4. Run data quality validation checks
5. Clean summary listings
6. Clean and aggregate calendar data
7. Clean and aggregate reviews data
8. Build the final listing master table
9. Build the DuckDB warehouse and analytics outputs

Run from project root:

    python -m src.pipeline_runner
"""

import time
from typing import Callable

from src.config import create_project_directories, get_project_status
from src.ingestion.raw_data_loader import (
    check_raw_files,
    load_all_tabular_raw_datasets,
)
from src.profiling.dataset_profiler import (
    create_dataset_inventory,
    create_schema_profile,
    create_missing_value_summary,
    save_profile_outputs,
)
from src.validation.data_quality_checks import run_data_quality_checks
from src.cleaning.listings_cleaner import run_summary_listings_cleaning
from src.cleaning.calendar_cleaner import run_calendar_cleaning
from src.cleaning.reviews_cleaner import run_reviews_cleaning
from src.transformation.listing_master_builder import run_listing_master_builder
from src.warehouse.duckdb_builder import run_duckdb_warehouse_builder


def run_step(step_name: str, step_function: Callable[[], None]) -> None:
    """
    Run a pipeline step with simple timing and status messages.

    Args:
        step_name: Human-readable step name.
        step_function: Function to execute.
    """
    print("\n" + "=" * 80)
    print(f"STARTING: {step_name}")
    print("=" * 80)

    start_time = time.time()

    step_function()

    end_time = time.time()
    elapsed_seconds = round(end_time - start_time, 2)

    print("-" * 80)
    print(f"COMPLETED: {step_name}")
    print(f"Elapsed time: {elapsed_seconds} seconds")
    print("-" * 80)


def run_raw_file_check() -> None:
    """
    Check expected raw files and print the inventory.
    """
    inventory = check_raw_files()
    print(inventory)

    missing_files = inventory[inventory["file_exists"] == False]

    if not missing_files.empty:
        raise FileNotFoundError(
            "Some raw files are missing. Please check the raw data folder."
        )


def run_dataset_profiling() -> None:
    """
    Generate dataset inventory, schema profile, and missing value summary.
    """
    datasets = load_all_tabular_raw_datasets()

    dataset_inventory = create_dataset_inventory(datasets)
    schema_profile = create_schema_profile(datasets)
    missing_value_summary = create_missing_value_summary(datasets)

    save_profile_outputs(
        dataset_inventory=dataset_inventory,
        schema_profile=schema_profile,
        missing_value_summary=missing_value_summary,
    )

    print("\nDataset inventory:")
    print(dataset_inventory)

    print("\nTop missing value rows:")
    print(missing_value_summary.head(15))


def run_pipeline() -> None:
    """
    Run the full project pipeline.
    """
    print("\nInside Airbnb Market Intelligence Platform")
    print("End-to-End Pipeline Runner")
    print("=" * 80)

    pipeline_start_time = time.time()

    run_step("Create project directories", create_project_directories)

    print("\nProject status:")
    for key, value in get_project_status().items():
        print(f"{key}: {value}")

    run_step("Check raw data files", run_raw_file_check)
    run_step("Generate dataset profiling reports", run_dataset_profiling)
    run_step("Run data quality validation checks", run_data_quality_checks)
    run_step("Clean summary listings", run_summary_listings_cleaning)
    run_step("Clean and aggregate calendar data", run_calendar_cleaning)
    run_step("Clean and aggregate reviews data", run_reviews_cleaning)
    run_step("Build final listing master table", run_listing_master_builder)
    run_step("Build DuckDB warehouse", run_duckdb_warehouse_builder)

    pipeline_end_time = time.time()
    total_elapsed_seconds = round(pipeline_end_time - pipeline_start_time, 2)
    total_elapsed_minutes = round(total_elapsed_seconds / 60, 2)

    print("\n" + "=" * 80)
    print("FULL PIPELINE COMPLETED SUCCESSFULLY")
    print(f"Total elapsed time: {total_elapsed_seconds} seconds")
    print(f"Total elapsed time: {total_elapsed_minutes} minutes")
    print("=" * 80)


if __name__ == "__main__":
    run_pipeline()