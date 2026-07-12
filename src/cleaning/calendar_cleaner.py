"""
Reusable cleaning and aggregation functions for the Inside Airbnb calendar dataset.

The raw calendar dataset contains one row per listing per date. This module
cleans availability values and aggregates the calendar into listing-level
availability and stay-policy metrics.

Important limitation:
The Amsterdam calendar file used in this project does not contain daily price
or adjusted_price columns. Therefore, this module focuses on availability and
minimum/maximum night metrics only.
"""

import numpy as np
import pandas as pd

from src.config import (
    RAW_FILES,
    PROCESSED_CITY_DIR,
    DATA_QUALITY_REPORTS_DIR,
)


def clean_available_flag(available_series: pd.Series) -> pd.Series:
    """
    Convert availability values into numeric flags.

    Expected raw values are usually:
    - 't' for available
    - 'f' for unavailable

    Returns:
        pd.Series: 1 for available, 0 for unavailable, NaN for invalid/missing.
    """
    return (
        available_series
        .astype(str)
        .str.strip()
        .str.lower()
        .map(
            {
                "t": 1,
                "true": 1,
                "1": 1,
                "f": 0,
                "false": 0,
                "0": 0,
            }
        )
    )


def clean_calendar(calendar: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw calendar dataset.

    Args:
        calendar: Raw calendar DataFrame.

    Returns:
        pd.DataFrame: Cleaned calendar DataFrame with standardized fields.
    """
    cleaned = calendar.copy()

    cleaned["listing_id"] = pd.to_numeric(cleaned["listing_id"], errors="coerce").astype("Int64")
    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")

    cleaned["available_flag"] = clean_available_flag(cleaned["available"])
    cleaned["unavailable_flag"] = np.where(
        cleaned["available_flag"].notna(),
        1 - cleaned["available_flag"],
        np.nan,
    )

    if "minimum_nights" in cleaned.columns:
        cleaned["minimum_nights"] = pd.to_numeric(cleaned["minimum_nights"], errors="coerce")

    if "maximum_nights" in cleaned.columns:
        cleaned["maximum_nights"] = pd.to_numeric(cleaned["maximum_nights"], errors="coerce")

    cleaned["is_weekend"] = cleaned["date"].dt.dayofweek.isin([5, 6])
    cleaned["is_weekday"] = cleaned["date"].dt.dayofweek.isin([0, 1, 2, 3, 4])

    cleaned["weekend_available_flag"] = np.where(
        cleaned["is_weekend"],
        cleaned["available_flag"],
        np.nan,
    )

    cleaned["weekday_available_flag"] = np.where(
        cleaned["is_weekday"],
        cleaned["available_flag"],
        np.nan,
    )

    return cleaned


def create_calendar_listing_metrics(cleaned_calendar: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate cleaned calendar data into listing-level metrics.

    Args:
        cleaned_calendar: Cleaned calendar DataFrame.

    Returns:
        pd.DataFrame: Listing-level calendar metrics.
    """
    calendar_metrics = (
        cleaned_calendar
        .groupby("listing_id", dropna=False)
        .agg(
            calendar_days=("date", "count"),
            calendar_start_date=("date", "min"),
            calendar_end_date=("date", "max"),
            available_days=("available_flag", "sum"),
            unavailable_days=("unavailable_flag", "sum"),
            availability_rate=("available_flag", "mean"),
            occupancy_proxy=("unavailable_flag", "mean"),
            weekend_availability_rate=("weekend_available_flag", "mean"),
            weekday_availability_rate=("weekday_available_flag", "mean"),
            avg_minimum_nights=("minimum_nights", "mean"),
            median_minimum_nights=("minimum_nights", "median"),
            avg_maximum_nights=("maximum_nights", "mean"),
            median_maximum_nights=("maximum_nights", "median"),
            missing_available_values=("available_flag", lambda values: int(values.isna().sum())),
        )
        .reset_index()
    )

    numeric_columns_to_round = [
        "availability_rate",
        "occupancy_proxy",
        "weekend_availability_rate",
        "weekday_availability_rate",
        "avg_minimum_nights",
        "median_minimum_nights",
        "avg_maximum_nights",
        "median_maximum_nights",
    ]

    for column in numeric_columns_to_round:
        if column in calendar_metrics.columns:
            calendar_metrics[column] = calendar_metrics[column].round(4)

    count_columns = [
        "available_days",
        "unavailable_days",
        "missing_available_values",
    ]

    for column in count_columns:
        calendar_metrics[column] = calendar_metrics[column].fillna(0).astype(int)

    return calendar_metrics


def create_calendar_cleaning_summary(
    raw_calendar: pd.DataFrame,
    cleaned_calendar: pd.DataFrame,
    calendar_metrics: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a summary report for calendar cleaning and aggregation.

    Args:
        raw_calendar: Raw calendar DataFrame.
        cleaned_calendar: Cleaned calendar DataFrame.
        calendar_metrics: Aggregated listing-level calendar metrics.

    Returns:
        pd.DataFrame: Calendar cleaning summary.
    """
    duplicate_listing_date_count = cleaned_calendar.duplicated(
        subset=["listing_id", "date"]
    ).sum()

    summary_rows = [
        {
            "metric": "raw_calendar_rows",
            "value": len(raw_calendar),
        },
        {
            "metric": "calendar_metric_rows",
            "value": len(calendar_metrics),
        },
        {
            "metric": "unique_listing_ids",
            "value": cleaned_calendar["listing_id"].nunique(dropna=True),
        },
        {
            "metric": "missing_listing_ids",
            "value": int(cleaned_calendar["listing_id"].isna().sum()),
        },
        {
            "metric": "missing_dates",
            "value": int(cleaned_calendar["date"].isna().sum()),
        },
        {
            "metric": "invalid_available_values",
            "value": int(cleaned_calendar["available_flag"].isna().sum()),
        },
        {
            "metric": "duplicate_listing_date_rows",
            "value": int(duplicate_listing_date_count),
        },
        {
            "metric": "minimum_calendar_days_per_listing",
            "value": int(calendar_metrics["calendar_days"].min()),
        },
        {
            "metric": "maximum_calendar_days_per_listing",
            "value": int(calendar_metrics["calendar_days"].max()),
        },
        {
            "metric": "average_availability_rate",
            "value": round(calendar_metrics["availability_rate"].mean(), 4),
        },
        {
            "metric": "average_occupancy_proxy",
            "value": round(calendar_metrics["occupancy_proxy"].mean(), 4),
        },
    ]

    return pd.DataFrame(summary_rows)


def run_calendar_cleaning() -> None:
    """
    Run calendar cleaning and save listing-level calendar metrics.
    """
    PROCESSED_CITY_DIR.mkdir(parents=True, exist_ok=True)
    DATA_QUALITY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading raw calendar data...")
    calendar = pd.read_csv(RAW_FILES["calendar"])

    print("Cleaning calendar data...")
    cleaned_calendar = clean_calendar(calendar)

    print("Creating listing-level calendar metrics...")
    calendar_metrics = create_calendar_listing_metrics(cleaned_calendar)

    print("Creating calendar cleaning summary...")
    cleaning_summary = create_calendar_cleaning_summary(
        raw_calendar=calendar,
        cleaned_calendar=cleaned_calendar,
        calendar_metrics=calendar_metrics,
    )

    metrics_output_path = PROCESSED_CITY_DIR / "calendar_listing_metrics_from_src.parquet"
    summary_output_path = DATA_QUALITY_REPORTS_DIR / "calendar_cleaning_summary_from_src.csv"

    calendar_metrics.to_parquet(metrics_output_path, index=False)
    cleaning_summary.to_csv(summary_output_path, index=False)

    print("\nCalendar cleaning summary:")
    print(cleaning_summary)

    print("\nCalendar metrics preview:")
    print(calendar_metrics.head())

    print(f"\nCalendar metrics saved to: {metrics_output_path}")
    print(f"Calendar cleaning summary saved to: {summary_output_path}")
    print("\nCalendar cleaning completed successfully.")


if __name__ == "__main__":
    run_calendar_cleaning()