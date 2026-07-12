"""
Reusable data quality validation checks for the Inside Airbnb project.

This module validates key data engineering assumptions across raw Inside Airbnb
datasets, including primary keys, relationship coverage, domain checks, and
basic value validity.
"""

from typing import Dict, List

import pandas as pd

from src.config import DATA_QUALITY_REPORTS_DIR
from src.ingestion.raw_data_loader import load_all_tabular_raw_datasets


def clean_price_series(price_series: pd.Series) -> pd.Series:
    """
    Convert a price column into numeric values.

    Handles both numeric prices and string prices such as "$1,200.00".
    """
    return pd.to_numeric(
        price_series.astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False),
        errors="coerce",
    )


def create_check_result(
    check_name: str,
    dataset_name: str,
    status: str,
    issue_count: int,
    total_count: int,
    notes: str,
) -> dict:
    """
    Create a standardized validation check result row.
    """
    issue_percentage = round((issue_count / total_count) * 100, 2) if total_count > 0 else 0

    return {
        "check_name": check_name,
        "dataset_name": dataset_name,
        "status": status,
        "issue_count": issue_count,
        "total_count": total_count,
        "issue_percentage": issue_percentage,
        "notes": notes,
    }


def validate_summary_listings(summary_listings: pd.DataFrame) -> List[dict]:
    """
    Validate the summary listings dataset.
    """
    results = []
    total_rows = len(summary_listings)

    missing_id_count = summary_listings["id"].isna().sum()
    results.append(
        create_check_result(
            check_name="missing_listing_id",
            dataset_name="summary_listings",
            status="PASS" if missing_id_count == 0 else "WARN",
            issue_count=int(missing_id_count),
            total_count=total_rows,
            notes="Listing ID should not be missing.",
        )
    )

    duplicate_id_count = summary_listings["id"].duplicated().sum()
    results.append(
        create_check_result(
            check_name="duplicate_listing_id",
            dataset_name="summary_listings",
            status="PASS" if duplicate_id_count == 0 else "WARN",
            issue_count=int(duplicate_id_count),
            total_count=total_rows,
            notes="Listing ID should be unique in summary listings.",
        )
    )

    if "price" in summary_listings.columns:
        price_numeric = clean_price_series(summary_listings["price"])
        missing_price_count = price_numeric.isna().sum()
        invalid_price_count = (price_numeric <= 0).sum()

        results.append(
            create_check_result(
                check_name="missing_price",
                dataset_name="summary_listings",
                status="WARN" if missing_price_count > 0 else "PASS",
                issue_count=int(missing_price_count),
                total_count=total_rows,
                notes="Missing prices reduce pricing and ML coverage.",
            )
        )

        results.append(
            create_check_result(
                check_name="invalid_non_positive_price",
                dataset_name="summary_listings",
                status="PASS" if invalid_price_count == 0 else "WARN",
                issue_count=int(invalid_price_count),
                total_count=total_rows,
                notes="Price should be greater than zero when available.",
            )
        )

    if {"latitude", "longitude"}.issubset(summary_listings.columns):
        invalid_coordinates = (
            summary_listings["latitude"].isna()
            | summary_listings["longitude"].isna()
            | ~summary_listings["latitude"].between(-90, 90)
            | ~summary_listings["longitude"].between(-180, 180)
        ).sum()

        results.append(
            create_check_result(
                check_name="invalid_coordinates",
                dataset_name="summary_listings",
                status="PASS" if invalid_coordinates == 0 else "WARN",
                issue_count=int(invalid_coordinates),
                total_count=total_rows,
                notes="Latitude and longitude should be present and valid.",
            )
        )

    if "availability_365" in summary_listings.columns:
        invalid_availability = (
            summary_listings["availability_365"].isna()
            | ~summary_listings["availability_365"].between(0, 365)
        ).sum()

        results.append(
            create_check_result(
                check_name="invalid_availability_365",
                dataset_name="summary_listings",
                status="PASS" if invalid_availability == 0 else "WARN",
                issue_count=int(invalid_availability),
                total_count=total_rows,
                notes="Availability should be between 0 and 365.",
            )
        )

    return results


def validate_calendar(calendar: pd.DataFrame) -> List[dict]:
    """
    Validate the calendar dataset.
    """
    results = []
    total_rows = len(calendar)

    missing_listing_id_count = calendar["listing_id"].isna().sum()
    results.append(
        create_check_result(
            check_name="missing_listing_id",
            dataset_name="calendar",
            status="PASS" if missing_listing_id_count == 0 else "WARN",
            issue_count=int(missing_listing_id_count),
            total_count=total_rows,
            notes="Calendar rows should have listing_id.",
        )
    )

    if "date" in calendar.columns:
        missing_date_count = calendar["date"].isna().sum()
        results.append(
            create_check_result(
                check_name="missing_calendar_date",
                dataset_name="calendar",
                status="PASS" if missing_date_count == 0 else "WARN",
                issue_count=int(missing_date_count),
                total_count=total_rows,
                notes="Calendar rows should have a date.",
            )
        )

    if "available" in calendar.columns:
        invalid_available_count = (~calendar["available"].isin(["t", "f", True, False])).sum()

        results.append(
            create_check_result(
                check_name="invalid_available_values",
                dataset_name="calendar",
                status="PASS" if invalid_available_count == 0 else "WARN",
                issue_count=int(invalid_available_count),
                total_count=total_rows,
                notes="Calendar availability should use expected boolean/t/f values.",
            )
        )

    if {"listing_id", "date"}.issubset(calendar.columns):
        duplicate_listing_date_count = calendar.duplicated(subset=["listing_id", "date"]).sum()

        results.append(
            create_check_result(
                check_name="duplicate_listing_date",
                dataset_name="calendar",
                status="PASS" if duplicate_listing_date_count == 0 else "WARN",
                issue_count=int(duplicate_listing_date_count),
                total_count=total_rows,
                notes="Each listing should have one row per date.",
            )
        )

    return results


def validate_reviews(detailed_reviews: pd.DataFrame) -> List[dict]:
    """
    Validate the detailed reviews dataset.
    """
    results = []
    total_rows = len(detailed_reviews)

    missing_listing_id_count = detailed_reviews["listing_id"].isna().sum()
    results.append(
        create_check_result(
            check_name="missing_listing_id",
            dataset_name="detailed_reviews",
            status="PASS" if missing_listing_id_count == 0 else "WARN",
            issue_count=int(missing_listing_id_count),
            total_count=total_rows,
            notes="Review rows should have listing_id.",
        )
    )

    if "id" in detailed_reviews.columns:
        duplicate_review_id_count = detailed_reviews["id"].duplicated().sum()

        results.append(
            create_check_result(
                check_name="duplicate_review_id",
                dataset_name="detailed_reviews",
                status="PASS" if duplicate_review_id_count == 0 else "WARN",
                issue_count=int(duplicate_review_id_count),
                total_count=total_rows,
                notes="Review ID should be unique.",
            )
        )

    if "comments" in detailed_reviews.columns:
        missing_comments_count = detailed_reviews["comments"].isna().sum()

        results.append(
            create_check_result(
                check_name="missing_review_comments",
                dataset_name="detailed_reviews",
                status="WARN" if missing_comments_count > 0 else "PASS",
                issue_count=int(missing_comments_count),
                total_count=total_rows,
                notes="Some reviews may not include written comments.",
            )
        )

    return results


def validate_relationship_coverage(datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Validate relationship coverage between listing master keys and related tables.
    """
    summary_listing_ids = set(datasets["summary_listings"]["id"].dropna())

    relationship_rows = []

    relationship_sources = {
        "calendar": "listing_id",
        "detailed_reviews": "listing_id",
        "summary_reviews": "listing_id",
    }

    for dataset_name, listing_id_column in relationship_sources.items():
        if dataset_name not in datasets:
            continue

        related_listing_ids = set(datasets[dataset_name][listing_id_column].dropna())
        matched_ids = related_listing_ids.intersection(summary_listing_ids)
        unmatched_ids = related_listing_ids.difference(summary_listing_ids)

        relationship_rows.append(
            {
                "related_dataset": dataset_name,
                "related_unique_listing_ids": len(related_listing_ids),
                "matched_listing_ids": len(matched_ids),
                "unmatched_listing_ids": len(unmatched_ids),
                "coverage_percentage": round(
                    (len(matched_ids) / len(related_listing_ids)) * 100, 2
                )
                if len(related_listing_ids) > 0
                else 0,
            }
        )

    return pd.DataFrame(relationship_rows)


def validate_neighbourhood_coverage(datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Validate whether listing neighbourhoods are covered by the neighbourhood lookup file.
    """
    summary_neighbourhoods = set(datasets["summary_listings"]["neighbourhood"].dropna())
    lookup_neighbourhoods = set(datasets["neighbourhoods"]["neighbourhood"].dropna())

    missing_in_lookup = summary_neighbourhoods.difference(lookup_neighbourhoods)
    unused_lookup_values = lookup_neighbourhoods.difference(summary_neighbourhoods)

    return pd.DataFrame(
        [
            {
                "check_name": "neighbourhood_lookup_coverage",
                "listing_neighbourhood_count": len(summary_neighbourhoods),
                "lookup_neighbourhood_count": len(lookup_neighbourhoods),
                "missing_in_lookup_count": len(missing_in_lookup),
                "unused_lookup_count": len(unused_lookup_values),
                "missing_in_lookup_values": " | ".join(sorted(missing_in_lookup)),
                "unused_lookup_values": " | ".join(sorted(unused_lookup_values)),
            }
        ]
    )


def run_data_quality_checks() -> None:
    """
    Run all reusable data quality checks and save results.
    """
    DATA_QUALITY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading raw datasets...")
    datasets = load_all_tabular_raw_datasets()

    validation_results = []

    print("Validating summary listings...")
    validation_results.extend(validate_summary_listings(datasets["summary_listings"]))

    print("Validating calendar...")
    validation_results.extend(validate_calendar(datasets["calendar"]))

    print("Validating detailed reviews...")
    validation_results.extend(validate_reviews(datasets["detailed_reviews"]))

    validation_summary = pd.DataFrame(validation_results)

    print("Validating relationship coverage...")
    relationship_coverage = validate_relationship_coverage(datasets)

    print("Validating neighbourhood coverage...")
    neighbourhood_coverage = validate_neighbourhood_coverage(datasets)

    validation_summary.to_csv(
        DATA_QUALITY_REPORTS_DIR / "data_quality_validation_from_src.csv",
        index=False,
    )

    relationship_coverage.to_csv(
        DATA_QUALITY_REPORTS_DIR / "relationship_coverage_from_src.csv",
        index=False,
    )

    neighbourhood_coverage.to_csv(
        DATA_QUALITY_REPORTS_DIR / "neighbourhood_coverage_from_src.csv",
        index=False,
    )

    print("\nValidation summary:")
    print(validation_summary)

    print("\nRelationship coverage:")
    print(relationship_coverage)

    print("\nNeighbourhood coverage:")
    print(neighbourhood_coverage)

    print("\nData quality validation completed successfully.")


if __name__ == "__main__":
    run_data_quality_checks()