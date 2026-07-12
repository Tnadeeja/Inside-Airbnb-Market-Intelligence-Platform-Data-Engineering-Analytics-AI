"""
Reusable cleaning functions for the Inside Airbnb summary listings dataset.

This module converts the raw summary listings file into a cleaner processed
listing table with standardized IDs, numeric prices, parsed dates, and
basic data quality flags.
"""

import pandas as pd

from src.config import (
    RAW_FILES,
    PROCESSED_CITY_DIR,
    DATA_QUALITY_REPORTS_DIR,
)


def clean_price_series(price_series: pd.Series) -> pd.Series:
    """
    Convert price values into numeric format.

    Handles values such as "$1,200.00" and normal numeric values.
    """
    return pd.to_numeric(
        price_series.astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False),
        errors="coerce",
    )


def clean_summary_listings(summary_listings: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw summary listings dataset.

    Args:
        summary_listings: Raw summary listings DataFrame.

    Returns:
        pd.DataFrame: Cleaned summary listings DataFrame.
    """
    cleaned = summary_listings.copy()

    # Standard listing key
    cleaned["listing_id"] = pd.to_numeric(cleaned["id"], errors="coerce").astype("Int64")

    # Price cleaning
    cleaned["price_numeric"] = clean_price_series(cleaned["price"])

    # Numeric columns
    numeric_columns = [
        "host_id",
        "latitude",
        "longitude",
        "minimum_nights",
        "number_of_reviews",
        "reviews_per_month",
        "calculated_host_listings_count",
        "availability_365",
        "number_of_reviews_ltm",
    ]

    for column in numeric_columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    # Date columns
    if "last_review" in cleaned.columns:
        cleaned["last_review"] = pd.to_datetime(cleaned["last_review"], errors="coerce")

    # Text cleanup
    text_columns = [
        "name",
        "host_name",
        "neighbourhood",
        "room_type",
        "license",
    ]

    for column in text_columns:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].astype("string").str.strip()

    # Data quality flags
    cleaned["has_valid_listing_id"] = cleaned["listing_id"].notna()
    cleaned["has_valid_price"] = cleaned["price_numeric"].notna() & (cleaned["price_numeric"] > 0)
    cleaned["has_valid_coordinates"] = (
        cleaned["latitude"].between(-90, 90)
        & cleaned["longitude"].between(-180, 180)
    )

    cleaned["has_reviews"] = cleaned["number_of_reviews"].fillna(0) > 0

    # Keep original row count but remove exact duplicate listing IDs if any exist
    cleaned = cleaned.drop_duplicates(subset=["listing_id"], keep="first")

    return cleaned


def create_listings_cleaning_summary(cleaned_listings: pd.DataFrame) -> pd.DataFrame:
    """
    Create a small cleaning summary report.

    Args:
        cleaned_listings: Cleaned summary listings DataFrame.

    Returns:
        pd.DataFrame: Cleaning summary metrics.
    """
    total_rows = len(cleaned_listings)

    summary_rows = [
        {
            "metric": "total_cleaned_rows",
            "value": total_rows,
        },
        {
            "metric": "unique_listing_ids",
            "value": cleaned_listings["listing_id"].nunique(dropna=True),
        },
        {
            "metric": "missing_listing_ids",
            "value": int(cleaned_listings["listing_id"].isna().sum()),
        },
        {
            "metric": "duplicate_listing_ids",
            "value": int(cleaned_listings["listing_id"].duplicated().sum()),
        },
        {
            "metric": "missing_or_invalid_prices",
            "value": int((~cleaned_listings["has_valid_price"]).sum()),
        },
        {
            "metric": "valid_price_rows",
            "value": int(cleaned_listings["has_valid_price"].sum()),
        },
        {
            "metric": "invalid_coordinates",
            "value": int((~cleaned_listings["has_valid_coordinates"]).sum()),
        },
        {
            "metric": "listings_with_reviews",
            "value": int(cleaned_listings["has_reviews"].sum()),
        },
        {
            "metric": "listings_without_reviews",
            "value": int((~cleaned_listings["has_reviews"]).sum()),
        },
    ]

    return pd.DataFrame(summary_rows)


def run_summary_listings_cleaning() -> None:
    """
    Run summary listings cleaning and save processed output.
    """
    PROCESSED_CITY_DIR.mkdir(parents=True, exist_ok=True)
    DATA_QUALITY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading raw summary listings...")
    summary_listings = pd.read_csv(RAW_FILES["summary_listings"])

    print("Cleaning summary listings...")
    cleaned_listings = clean_summary_listings(summary_listings)

    print("Creating cleaning summary...")
    cleaning_summary = create_listings_cleaning_summary(cleaned_listings)

    processed_output_path = PROCESSED_CITY_DIR / "summary_listings_clean_from_src.parquet"
    summary_output_path = DATA_QUALITY_REPORTS_DIR / "summary_listings_cleaning_summary_from_src.csv"

    cleaned_listings.to_parquet(processed_output_path, index=False)
    cleaning_summary.to_csv(summary_output_path, index=False)

    print("\nCleaning summary:")
    print(cleaning_summary)

    print(f"\nCleaned listings saved to: {processed_output_path}")
    print(f"Cleaning summary saved to: {summary_output_path}")
    print("\nSummary listings cleaning completed successfully.")


if __name__ == "__main__":
    run_summary_listings_cleaning()