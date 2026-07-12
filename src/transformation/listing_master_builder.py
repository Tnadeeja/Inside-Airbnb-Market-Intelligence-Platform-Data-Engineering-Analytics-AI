"""
Build the final listing master table for the Inside Airbnb project.

This module combines cleaned summary listings, detailed listing attributes,
calendar availability metrics, review activity metrics, and neighbourhood-level
market metrics into one analytical listing master table.
"""

import ast
from typing import List

import numpy as np
import pandas as pd

from src.config import (
    RAW_FILES,
    PROCESSED_CITY_DIR,
    DATA_QUALITY_REPORTS_DIR,
)


def safe_read_parquet(file_path):
    """
    Read a parquet file and raise a clear error if it does not exist.
    """
    if not file_path.exists():
        raise FileNotFoundError(
            f"Required processed file not found: {file_path}. "
            "Please run the related cleaning script first."
        )

    return pd.read_parquet(file_path)


def parse_amenities_count(value) -> int:
    """
    Estimate amenities count from an amenities field.

    Inside Airbnb amenities are commonly stored as a list-like string.
    This function handles list strings, normal strings, missing values,
    and malformed values safely.
    """
    if pd.isna(value):
        return 0

    value_as_string = str(value).strip()

    if value_as_string in ["", "[]"]:
        return 0

    try:
        parsed_value = ast.literal_eval(value_as_string)
        if isinstance(parsed_value, list):
            return len(parsed_value)
    except (ValueError, SyntaxError):
        pass

    return len([item for item in value_as_string.split(",") if item.strip()])


def standardize_boolean_column(series: pd.Series) -> pd.Series:
    """
    Standardize Airbnb boolean-style columns into readable string values.
    """
    return (
        series
        .astype("string")
        .str.strip()
        .str.lower()
        .map(
            {
                "t": "true",
                "true": "true",
                "1": "true",
                "f": "false",
                "false": "false",
                "0": "false",
            }
        )
        .fillna("missing")
    )


def select_existing_columns(dataframe: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Select only columns that exist in a DataFrame.
    This keeps the pipeline safe if some columns are unavailable.
    """
    existing_columns = [column for column in columns if column in dataframe.columns]
    return dataframe[existing_columns].copy()


def prepare_detailed_listing_features(detailed_listings: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare selected detailed listing features for enrichment.

    Args:
        detailed_listings: Raw detailed listings DataFrame.

    Returns:
        pd.DataFrame: Listing-level detailed feature table.
    """
    detailed = detailed_listings.copy()

    detailed["listing_id"] = pd.to_numeric(detailed["id"], errors="coerce").astype("Int64")

    selected_columns = [
        "listing_id",
        "property_type",
        "accommodates",
        "bathrooms",
        "bedrooms",
        "beds",
        "amenities",
        "host_since",
        "host_is_superhost",
        "host_identity_verified",
        "instant_bookable",
        "review_scores_rating",
        "review_scores_accuracy",
        "review_scores_cleanliness",
        "review_scores_checkin",
        "review_scores_communication",
        "review_scores_location",
        "review_scores_value",
    ]

    detailed_features = select_existing_columns(detailed, selected_columns)

    numeric_columns = [
        "accommodates",
        "bathrooms",
        "bedrooms",
        "beds",
        "review_scores_rating",
        "review_scores_accuracy",
        "review_scores_cleanliness",
        "review_scores_checkin",
        "review_scores_communication",
        "review_scores_location",
        "review_scores_value",
    ]

    for column in numeric_columns:
        if column in detailed_features.columns:
            detailed_features[column] = pd.to_numeric(detailed_features[column], errors="coerce")

    if "amenities" in detailed_features.columns:
        detailed_features["amenities_count"] = detailed_features["amenities"].apply(parse_amenities_count)
        detailed_features = detailed_features.drop(columns=["amenities"])

    if "host_since" in detailed_features.columns:
        detailed_features["host_since"] = pd.to_datetime(
            detailed_features["host_since"],
            errors="coerce",
        )

    boolean_columns = [
        "host_is_superhost",
        "host_identity_verified",
        "instant_bookable",
    ]

    for column in boolean_columns:
        if column in detailed_features.columns:
            detailed_features[column] = standardize_boolean_column(detailed_features[column])

    detailed_features = detailed_features.drop_duplicates(subset=["listing_id"], keep="first")

    return detailed_features


def create_neighbourhood_metrics(listing_master: pd.DataFrame) -> pd.DataFrame:
    """
    Create neighbourhood-level market metrics from the listing master base table.
    """
    neighbourhood_metrics = (
        listing_master
        .groupby("neighbourhood", dropna=False)
        .agg(
            neighbourhood_listing_count=("listing_id", "count"),
            neighbourhood_avg_price=("price_numeric", "mean"),
            neighbourhood_median_price=("price_numeric", "median"),
            neighbourhood_avg_availability_rate=("availability_rate", "mean"),
            neighbourhood_avg_occupancy_proxy=("occupancy_proxy", "mean"),
            neighbourhood_total_reviews=("number_of_reviews", "sum"),
        )
        .reset_index()
    )

    round_columns = [
        "neighbourhood_avg_price",
        "neighbourhood_median_price",
        "neighbourhood_avg_availability_rate",
        "neighbourhood_avg_occupancy_proxy",
    ]

    for column in round_columns:
        neighbourhood_metrics[column] = neighbourhood_metrics[column].round(4)

    return neighbourhood_metrics


def add_host_portfolio_segment(listing_master: pd.DataFrame) -> pd.DataFrame:
    """
    Add host portfolio segment using calculated host listing count.
    """
    output = listing_master.copy()

    if "calculated_host_listings_count" not in output.columns:
        output["host_portfolio_segment"] = "Unknown"
        return output

    conditions = [
        output["calculated_host_listings_count"].isna(),
        output["calculated_host_listings_count"] == 1,
        output["calculated_host_listings_count"].between(2, 5),
        output["calculated_host_listings_count"].between(6, 20),
        output["calculated_host_listings_count"] > 20,
    ]

    choices = [
        "Unknown Host",
        "Single-listing Host",
        "Small Portfolio Host",
        "Medium Portfolio Host",
        "Large Portfolio Host",
    ]

    output["host_portfolio_segment"] = np.select(
        conditions,
        choices,
        default="Unknown Host",
    )

    return output


def add_availability_segment(listing_master: pd.DataFrame) -> pd.DataFrame:
    """
    Add availability segment using listing-level availability rate.
    """
    output = listing_master.copy()

    if "availability_rate" not in output.columns:
        output["availability_segment"] = "Unknown"
        return output

    conditions = [
        output["availability_rate"].isna(),
        output["availability_rate"] <= 0.10,
        output["availability_rate"].between(0.10, 0.50, inclusive="right"),
        output["availability_rate"] > 0.50,
    ]

    choices = [
        "Unknown",
        "Low Availability",
        "Medium Availability",
        "High Availability",
    ]

    output["availability_segment"] = np.select(
        conditions,
        choices,
        default="Unknown",
    )

    return output


def build_listing_master() -> pd.DataFrame:
    """
    Build the final listing master table.

    Returns:
        pd.DataFrame: Final listing master table.
    """
    summary_clean_path = PROCESSED_CITY_DIR / "summary_listings_clean_from_src.parquet"
    calendar_metrics_path = PROCESSED_CITY_DIR / "calendar_listing_metrics_from_src.parquet"
    review_metrics_path = PROCESSED_CITY_DIR / "review_listing_metrics_from_src.parquet"

    print("Loading processed summary listings...")
    summary_clean = safe_read_parquet(summary_clean_path)

    print("Loading calendar metrics...")
    calendar_metrics = safe_read_parquet(calendar_metrics_path)

    print("Loading review metrics...")
    review_metrics = safe_read_parquet(review_metrics_path)

    print("Loading raw detailed listings...")
    detailed_listings = pd.read_csv(RAW_FILES["detailed_listings"])

    print("Preparing detailed listing features...")
    detailed_features = prepare_detailed_listing_features(detailed_listings)

    print("Joining summary listings with detailed listing features...")
    listing_master = summary_clean.merge(
        detailed_features,
        on="listing_id",
        how="left",
    )

    print("Joining calendar metrics...")
    listing_master = listing_master.merge(
        calendar_metrics,
        on="listing_id",
        how="left",
    )

    print("Joining review metrics...")
    listing_master = listing_master.merge(
        review_metrics,
        on="listing_id",
        how="left",
    )

    print("Adding default values for missing review and calendar metrics...")

    review_count_columns = [
        "detailed_review_count",
        "unique_reviewer_count",
        "detailed_reviews_last_365d",
        "reviews_with_comments",
    ]

    for column in review_count_columns:
        if column in listing_master.columns:
            listing_master[column] = listing_master[column].fillna(0).astype(int)

    calendar_count_columns = [
        "calendar_days",
        "available_days",
        "unavailable_days",
        "missing_available_values",
    ]

    for column in calendar_count_columns:
        if column in listing_master.columns:
            listing_master[column] = listing_master[column].fillna(0).astype(int)

    rate_columns = [
        "availability_rate",
        "occupancy_proxy",
        "weekend_availability_rate",
        "weekday_availability_rate",
        "comment_coverage_rate",
        "review_active_years",
        "avg_reviews_per_year",
    ]

    for column in rate_columns:
        if column in listing_master.columns:
            listing_master[column] = listing_master[column].fillna(0)

    print("Adding host portfolio and availability segments...")
    listing_master = add_host_portfolio_segment(listing_master)
    listing_master = add_availability_segment(listing_master)

    print("Creating neighbourhood metrics...")
    neighbourhood_metrics = create_neighbourhood_metrics(listing_master)

    print("Joining neighbourhood metrics...")
    listing_master = listing_master.merge(
        neighbourhood_metrics,
        on="neighbourhood",
        how="left",
    )

    return listing_master


def create_listing_master_summary(listing_master: pd.DataFrame) -> pd.DataFrame:
    """
    Create final listing master validation summary.
    """
    summary_rows = [
        {
            "metric": "listing_master_rows",
            "value": len(listing_master),
        },
        {
            "metric": "listing_master_columns",
            "value": listing_master.shape[1],
        },
        {
            "metric": "unique_listing_ids",
            "value": listing_master["listing_id"].nunique(dropna=True),
        },
        {
            "metric": "duplicate_listing_ids",
            "value": int(listing_master["listing_id"].duplicated().sum()),
        },
        {
            "metric": "valid_price_rows",
            "value": int(listing_master["has_valid_price"].sum()),
        },
        {
            "metric": "missing_or_invalid_price_rows",
            "value": int((~listing_master["has_valid_price"]).sum()),
        },
        {
            "metric": "listings_with_calendar_metrics",
            "value": int((listing_master["calendar_days"] > 0).sum()),
        },
        {
            "metric": "listings_with_review_metrics",
            "value": int((listing_master["detailed_review_count"] > 0).sum()),
        },
        {
            "metric": "listings_with_detailed_features",
            "value": int(listing_master["property_type"].notna().sum())
            if "property_type" in listing_master.columns
            else 0,
        },
        {
            "metric": "neighbourhood_count",
            "value": listing_master["neighbourhood"].nunique(dropna=True),
        },
    ]

    return pd.DataFrame(summary_rows)


def run_listing_master_builder() -> None:
    """
    Build and save the final listing master table.
    """
    PROCESSED_CITY_DIR.mkdir(parents=True, exist_ok=True)
    DATA_QUALITY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Building final listing master...")
    listing_master = build_listing_master()

    print("Creating listing master summary...")
    listing_master_summary = create_listing_master_summary(listing_master)

    listing_master_output_path = PROCESSED_CITY_DIR / "listing_master_final_from_src.parquet"
    summary_output_path = DATA_QUALITY_REPORTS_DIR / "listing_master_summary_from_src.csv"

    listing_master.to_parquet(listing_master_output_path, index=False)
    listing_master_summary.to_csv(summary_output_path, index=False)

    print("\nListing master summary:")
    print(listing_master_summary)

    print("\nListing master preview:")
    preview_columns = [
        "listing_id",
        "name",
        "room_type",
        "neighbourhood",
        "price_numeric",
        "availability_rate",
        "occupancy_proxy",
        "detailed_review_count",
        "host_portfolio_segment",
        "availability_segment",
    ]

    existing_preview_columns = [
        column for column in preview_columns if column in listing_master.columns
    ]

    print(listing_master[existing_preview_columns].head())

    print(f"\nFinal listing master saved to: {listing_master_output_path}")
    print(f"Listing master summary saved to: {summary_output_path}")
    print("\nFinal listing master build completed successfully.")


if __name__ == "__main__":
    run_listing_master_builder()