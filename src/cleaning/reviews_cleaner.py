"""
Reusable cleaning and aggregation functions for the Inside Airbnb detailed reviews dataset.

This module cleans review IDs, listing IDs, review dates, reviewer information,
and review comments. It then aggregates detailed reviews into listing-level
review activity metrics.
"""

import numpy as np
import pandas as pd

from src.config import (
    RAW_FILES,
    SNAPSHOT_DATE,
    PROCESSED_CITY_DIR,
    DATA_QUALITY_REPORTS_DIR,
)


def clean_reviews(detailed_reviews: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw detailed reviews dataset.

    Args:
        detailed_reviews: Raw detailed reviews DataFrame.

    Returns:
        pd.DataFrame: Cleaned detailed reviews DataFrame.
    """
    cleaned = detailed_reviews.copy()

    cleaned["listing_id"] = pd.to_numeric(cleaned["listing_id"], errors="coerce").astype("Int64")

    if "id" in cleaned.columns:
        cleaned["review_id"] = pd.to_numeric(cleaned["id"], errors="coerce").astype("Int64")

    if "reviewer_id" in cleaned.columns:
        cleaned["reviewer_id"] = pd.to_numeric(cleaned["reviewer_id"], errors="coerce").astype("Int64")

    if "date" in cleaned.columns:
        cleaned["review_date"] = pd.to_datetime(cleaned["date"], errors="coerce")

    if "reviewer_name" in cleaned.columns:
        cleaned["reviewer_name"] = cleaned["reviewer_name"].astype("string").str.strip()

    if "comments" in cleaned.columns:
        cleaned["comments"] = cleaned["comments"].astype("string")
        cleaned["has_comment"] = cleaned["comments"].notna() & (cleaned["comments"].str.strip() != "")
        cleaned["comment_length"] = cleaned["comments"].fillna("").astype(str).str.len()
    else:
        cleaned["has_comment"] = False
        cleaned["comment_length"] = 0

    snapshot_date = pd.to_datetime(SNAPSHOT_DATE)
    last_365_days_start = snapshot_date - pd.Timedelta(days=365)

    cleaned["is_review_last_365_days"] = (
        cleaned["review_date"].notna()
        & (cleaned["review_date"] >= last_365_days_start)
        & (cleaned["review_date"] <= snapshot_date)
    )

    return cleaned


def create_review_listing_metrics(cleaned_reviews: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate cleaned detailed reviews into listing-level metrics.

    Args:
        cleaned_reviews: Cleaned detailed reviews DataFrame.

    Returns:
        pd.DataFrame: Listing-level review metrics.
    """
    review_metrics = (
        cleaned_reviews
        .groupby("listing_id", dropna=False)
        .agg(
            detailed_review_count=("review_id", "count"),
            unique_reviewer_count=("reviewer_id", "nunique"),
            first_review_date=("review_date", "min"),
            last_review_date=("review_date", "max"),
            detailed_reviews_last_365d=("is_review_last_365_days", "sum"),
            reviews_with_comments=("has_comment", "sum"),
            average_comment_length=("comment_length", "mean"),
            median_comment_length=("comment_length", "median"),
        )
        .reset_index()
    )

    review_metrics["comment_coverage_rate"] = np.where(
        review_metrics["detailed_review_count"] > 0,
        review_metrics["reviews_with_comments"] / review_metrics["detailed_review_count"],
        0,
    )

    review_active_days = (
        review_metrics["last_review_date"] - review_metrics["first_review_date"]
    ).dt.days + 1

    review_metrics["review_active_years"] = (review_active_days / 365.25).replace(0, np.nan)

    review_metrics["avg_reviews_per_year"] = np.where(
        review_metrics["review_active_years"].notna(),
        review_metrics["detailed_review_count"] / review_metrics["review_active_years"],
        0,
    )

    round_columns = [
        "average_comment_length",
        "median_comment_length",
        "comment_coverage_rate",
        "review_active_years",
        "avg_reviews_per_year",
    ]

    for column in round_columns:
        review_metrics[column] = review_metrics[column].round(4)

    integer_columns = [
        "detailed_review_count",
        "unique_reviewer_count",
        "detailed_reviews_last_365d",
        "reviews_with_comments",
    ]

    for column in integer_columns:
        review_metrics[column] = review_metrics[column].fillna(0).astype(int)

    return review_metrics


def create_reviews_cleaning_summary(
    raw_reviews: pd.DataFrame,
    cleaned_reviews: pd.DataFrame,
    review_metrics: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a summary report for review cleaning and aggregation.

    Args:
        raw_reviews: Raw detailed reviews DataFrame.
        cleaned_reviews: Cleaned detailed reviews DataFrame.
        review_metrics: Listing-level review metrics DataFrame.

    Returns:
        pd.DataFrame: Review cleaning summary.
    """
    duplicate_review_id_count = (
        cleaned_reviews["review_id"].duplicated().sum()
        if "review_id" in cleaned_reviews.columns
        else 0
    )

    summary_rows = [
        {
            "metric": "raw_review_rows",
            "value": len(raw_reviews),
        },
        {
            "metric": "cleaned_review_rows",
            "value": len(cleaned_reviews),
        },
        {
            "metric": "review_metric_rows",
            "value": len(review_metrics),
        },
        {
            "metric": "unique_review_ids",
            "value": cleaned_reviews["review_id"].nunique(dropna=True),
        },
        {
            "metric": "duplicate_review_ids",
            "value": int(duplicate_review_id_count),
        },
        {
            "metric": "unique_listing_ids_with_reviews",
            "value": cleaned_reviews["listing_id"].nunique(dropna=True),
        },
        {
            "metric": "missing_listing_ids",
            "value": int(cleaned_reviews["listing_id"].isna().sum()),
        },
        {
            "metric": "missing_review_ids",
            "value": int(cleaned_reviews["review_id"].isna().sum()),
        },
        {
            "metric": "missing_review_dates",
            "value": int(cleaned_reviews["review_date"].isna().sum()),
        },
        {
            "metric": "missing_review_comments",
            "value": int((~cleaned_reviews["has_comment"]).sum()),
        },
        {
            "metric": "reviews_with_comments",
            "value": int(cleaned_reviews["has_comment"].sum()),
        },
        {
            "metric": "reviews_last_365_days",
            "value": int(cleaned_reviews["is_review_last_365_days"].sum()),
        },
        {
            "metric": "max_reviews_for_single_listing",
            "value": int(review_metrics["detailed_review_count"].max()),
        },
        {
            "metric": "average_reviews_per_reviewed_listing",
            "value": round(review_metrics["detailed_review_count"].mean(), 2),
        },
    ]

    return pd.DataFrame(summary_rows)


def run_reviews_cleaning() -> None:
    """
    Run detailed reviews cleaning and save listing-level review metrics.
    """
    PROCESSED_CITY_DIR.mkdir(parents=True, exist_ok=True)
    DATA_QUALITY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading raw detailed reviews...")
    detailed_reviews = pd.read_csv(RAW_FILES["detailed_reviews"])

    print("Cleaning detailed reviews...")
    cleaned_reviews = clean_reviews(detailed_reviews)

    print("Creating listing-level review metrics...")
    review_metrics = create_review_listing_metrics(cleaned_reviews)

    print("Creating reviews cleaning summary...")
    cleaning_summary = create_reviews_cleaning_summary(
        raw_reviews=detailed_reviews,
        cleaned_reviews=cleaned_reviews,
        review_metrics=review_metrics,
    )

    metrics_output_path = PROCESSED_CITY_DIR / "review_listing_metrics_from_src.parquet"
    summary_output_path = DATA_QUALITY_REPORTS_DIR / "reviews_cleaning_summary_from_src.csv"

    review_metrics.to_parquet(metrics_output_path, index=False)
    cleaning_summary.to_csv(summary_output_path, index=False)

    print("\nReviews cleaning summary:")
    print(cleaning_summary)

    print("\nReview metrics preview:")
    print(review_metrics.head())

    print(f"\nReview metrics saved to: {metrics_output_path}")
    print(f"Reviews cleaning summary saved to: {summary_output_path}")
    print("\nReviews cleaning completed successfully.")


if __name__ == "__main__":
    run_reviews_cleaning()