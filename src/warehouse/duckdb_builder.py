"""
DuckDB warehouse builder for the Inside Airbnb Market Intelligence project.

This module creates a reusable analytical warehouse from the final listing master
table. It builds a simple star schema and analytical summary tables.
"""

import duckdb
import pandas as pd

from src.config import (
    PROCESSED_CITY_DIR,
    WAREHOUSE_DIR,
    DUCKDB_DATABASE_PATH,
    REPORTS_DIR,
)


ANALYTICS_OUTPUTS_DIR = REPORTS_DIR / "analytics_outputs"
DATA_QUALITY_REPORTS_DIR = REPORTS_DIR / "data_quality"


def get_listing_master_path():
    """
    Return the preferred listing master path.

    The src-generated listing master is preferred. If it does not exist,
    this function falls back to the notebook-generated listing master.
    """
    src_listing_master_path = PROCESSED_CITY_DIR / "listing_master_final_from_src.parquet"
    notebook_listing_master_path = PROCESSED_CITY_DIR / "listing_master_final.parquet"

    if src_listing_master_path.exists():
        return src_listing_master_path

    if notebook_listing_master_path.exists():
        return notebook_listing_master_path

    raise FileNotFoundError(
        "No final listing master parquet file found. "
        "Run src.transformation.listing_master_builder first."
    )


def create_base_table(connection: duckdb.DuckDBPyConnection, listing_master_path) -> None:
    """
    Create the base listing master table inside DuckDB.
    """
    connection.execute(
        f"""
        CREATE OR REPLACE TABLE listing_master_final AS
        SELECT *
        FROM read_parquet('{listing_master_path.as_posix()}')
        """
    )


def create_star_schema(connection: duckdb.DuckDBPyConnection) -> None:
    """
    Create dimension and fact tables for analytical querying.
    """

    connection.execute(
        """
        CREATE OR REPLACE TABLE dim_listing AS
        SELECT
            ROW_NUMBER() OVER (ORDER BY listing_id) AS listing_key,
            listing_id,
            name AS listing_name,
            room_type,
            property_type,
            minimum_nights,
            accommodates,
            bathrooms,
            bedrooms,
            beds,
            amenities_count,
            has_valid_price,
            has_valid_coordinates,
            license
        FROM listing_master_final
        """
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE dim_host AS
        WITH real_hosts AS (
            SELECT
                CAST(host_id AS BIGINT) AS host_id,
                ANY_VALUE(host_name) AS host_name,
                ANY_VALUE(host_since) AS host_since,
                ANY_VALUE(host_is_superhost) AS host_is_superhost,
                ANY_VALUE(host_identity_verified) AS host_identity_verified,
                MAX(calculated_host_listings_count) AS calculated_host_listings_count,
                ANY_VALUE(host_portfolio_segment) AS host_portfolio_segment
            FROM listing_master_final
            WHERE host_id IS NOT NULL
            GROUP BY CAST(host_id AS BIGINT)
        ),
        numbered_hosts AS (
            SELECT
                ROW_NUMBER() OVER (ORDER BY host_id) AS host_key,
                host_id,
                host_name,
                host_since,
                host_is_superhost,
                host_identity_verified,
                calculated_host_listings_count,
                host_portfolio_segment
            FROM real_hosts
        )
        SELECT
            -1 AS host_key,
            CAST(NULL AS BIGINT) AS host_id,
            'Unknown Host' AS host_name,
            CAST(NULL AS TIMESTAMP) AS host_since,
            'missing' AS host_is_superhost,
            'missing' AS host_identity_verified,
            CAST(NULL AS DOUBLE) AS calculated_host_listings_count,
            'Unknown Host' AS host_portfolio_segment

        UNION ALL

        SELECT
            host_key,
            host_id,
            host_name,
            host_since,
            host_is_superhost,
            host_identity_verified,
            calculated_host_listings_count,
            host_portfolio_segment
        FROM numbered_hosts
        """
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE dim_neighbourhood AS
        SELECT
            ROW_NUMBER() OVER (ORDER BY neighbourhood) AS neighbourhood_key,
            neighbourhood,
            ANY_VALUE(neighbourhood_group) AS neighbourhood_group,
            MAX(neighbourhood_listing_count) AS neighbourhood_listing_count,
            MAX(neighbourhood_avg_price) AS neighbourhood_avg_price,
            MAX(neighbourhood_median_price) AS neighbourhood_median_price,
            MAX(neighbourhood_avg_availability_rate) AS neighbourhood_avg_availability_rate,
            MAX(neighbourhood_avg_occupancy_proxy) AS neighbourhood_avg_occupancy_proxy,
            MAX(neighbourhood_total_reviews) AS neighbourhood_total_reviews
        FROM listing_master_final
        GROUP BY neighbourhood
        """
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE fact_listing_market AS
        SELECT
            ROW_NUMBER() OVER (ORDER BY lm.listing_id) AS fact_key,
            dl.listing_key,
            COALESCE(dh.host_key, -1) AS host_key,
            dn.neighbourhood_key,
            lm.listing_id,

            lm.price_numeric,
            lm.has_valid_price,

            lm.calendar_days,
            lm.available_days,
            lm.unavailable_days,
            lm.availability_rate,
            lm.occupancy_proxy,
            lm.weekend_availability_rate,
            lm.weekday_availability_rate,

            lm.number_of_reviews,
            lm.reviews_per_month,
            lm.detailed_review_count,
            lm.unique_reviewer_count,
            lm.detailed_reviews_last_365d,
            lm.avg_reviews_per_year,
            lm.comment_coverage_rate,

            lm.review_scores_rating,
            lm.review_scores_cleanliness,
            lm.review_scores_location,
            lm.review_scores_value,

            CASE
                WHEN lm.price_numeric IS NOT NULL
                     AND lm.price_numeric > 0
                     AND lm.unavailable_days IS NOT NULL
                THEN lm.price_numeric * lm.unavailable_days
                ELSE NULL
            END AS estimated_revenue_proxy

        FROM listing_master_final lm
        LEFT JOIN dim_listing dl
            ON lm.listing_id = dl.listing_id
        LEFT JOIN dim_host dh
            ON CAST(lm.host_id AS BIGINT) = dh.host_id
        LEFT JOIN dim_neighbourhood dn
            ON lm.neighbourhood = dn.neighbourhood
        """
    )


def create_analytics_tables(connection: duckdb.DuckDBPyConnection) -> None:
    """
    Create reusable analytical summary tables.
    """

    connection.execute(
        """
        CREATE OR REPLACE TABLE market_overview AS
        SELECT
            COUNT(*) AS total_listings,
            COUNT(DISTINCT CASE WHEN host_key != -1 THEN host_key END) AS total_known_hosts,
            COUNT(DISTINCT neighbourhood_key) AS total_neighbourhoods,
            ROUND(AVG(price_numeric), 2) AS avg_listing_price,
            ROUND(MEDIAN(price_numeric), 2) AS median_listing_price,
            ROUND(AVG(availability_rate), 4) AS avg_availability_rate,
            ROUND(AVG(occupancy_proxy), 4) AS avg_occupancy_proxy,
            SUM(CASE WHEN detailed_review_count > 0 THEN 1 ELSE 0 END) AS listings_with_reviews,
            SUM(CASE WHEN detailed_review_count = 0 THEN 1 ELSE 0 END) AS listings_without_reviews,
            SUM(detailed_review_count) AS total_detailed_reviews,
            ROUND(AVG(review_scores_rating), 2) AS avg_review_score,
            ROUND(SUM(estimated_revenue_proxy), 2) AS total_estimated_revenue_proxy,
            SUM(CASE WHEN has_valid_price = FALSE THEN 1 ELSE 0 END) AS listings_missing_or_invalid_price
        FROM fact_listing_market
        """
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE room_type_summary AS
        SELECT
            dl.room_type,
            COUNT(*) AS listing_count,
            ROUND(AVG(f.price_numeric), 2) AS avg_price,
            ROUND(MEDIAN(f.price_numeric), 2) AS median_price,
            ROUND(AVG(f.availability_rate), 4) AS avg_availability_rate,
            ROUND(AVG(f.occupancy_proxy), 4) AS avg_occupancy_proxy,
            SUM(f.detailed_review_count) AS total_detailed_reviews,
            ROUND(SUM(f.estimated_revenue_proxy), 2) AS total_estimated_revenue_proxy
        FROM fact_listing_market f
        LEFT JOIN dim_listing dl
            ON f.listing_key = dl.listing_key
        GROUP BY dl.room_type
        ORDER BY listing_count DESC
        """
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE neighbourhood_summary AS
        SELECT
            dn.neighbourhood,
            COUNT(*) AS listing_count,
            ROUND(AVG(f.price_numeric), 2) AS avg_price,
            ROUND(MEDIAN(f.price_numeric), 2) AS median_price,
            ROUND(AVG(f.availability_rate), 4) AS avg_availability_rate,
            ROUND(AVG(f.occupancy_proxy), 4) AS avg_occupancy_proxy,
            SUM(f.detailed_review_count) AS total_detailed_reviews,
            ROUND(SUM(f.estimated_revenue_proxy), 2) AS total_estimated_revenue_proxy
        FROM fact_listing_market f
        LEFT JOIN dim_neighbourhood dn
            ON f.neighbourhood_key = dn.neighbourhood_key
        GROUP BY dn.neighbourhood
        ORDER BY total_estimated_revenue_proxy DESC NULLS LAST
        """
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE host_portfolio_summary AS
        SELECT
            dh.host_portfolio_segment,
            COUNT(*) AS listing_count,
            COUNT(DISTINCT CASE WHEN dh.host_key != -1 THEN dh.host_key END) AS host_count,
            ROUND(AVG(f.price_numeric), 2) AS avg_price,
            ROUND(MEDIAN(f.price_numeric), 2) AS median_price,
            ROUND(AVG(f.availability_rate), 4) AS avg_availability_rate,
            ROUND(AVG(f.occupancy_proxy), 4) AS avg_occupancy_proxy,
            ROUND(SUM(f.estimated_revenue_proxy), 2) AS total_estimated_revenue_proxy
        FROM fact_listing_market f
        LEFT JOIN dim_host dh
            ON f.host_key = dh.host_key
        GROUP BY dh.host_portfolio_segment
        ORDER BY listing_count DESC
        """
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE review_score_summary AS
        WITH scored AS (
            SELECT
                CASE
                    WHEN review_scores_rating IS NULL THEN 'No rating'
                    WHEN review_scores_rating >= 4.8 THEN 'Excellent'
                    WHEN review_scores_rating >= 4.5 THEN 'Very good'
                    WHEN review_scores_rating >= 4.0 THEN 'Good'
                    ELSE 'Below 4.0'
                END AS review_score_band,
                *
            FROM fact_listing_market
        )
        SELECT
            review_score_band,
            COUNT(*) AS listing_count,
            ROUND(AVG(price_numeric), 2) AS avg_price,
            ROUND(MEDIAN(price_numeric), 2) AS median_price,
            ROUND(AVG(availability_rate), 4) AS avg_availability_rate,
            ROUND(AVG(occupancy_proxy), 4) AS avg_occupancy_proxy,
            SUM(detailed_review_count) AS total_detailed_reviews,
            ROUND(SUM(estimated_revenue_proxy), 2) AS total_estimated_revenue_proxy
        FROM scored
        GROUP BY review_score_band
        ORDER BY listing_count DESC
        """
    )


def create_table_summary(connection: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """
    Create row-count summary for warehouse tables.
    """
    table_names = [
        "listing_master_final",
        "dim_listing",
        "dim_host",
        "dim_neighbourhood",
        "fact_listing_market",
        "market_overview",
        "room_type_summary",
        "neighbourhood_summary",
        "host_portfolio_summary",
        "review_score_summary",
    ]

    rows = []

    for table_name in table_names:
        row_count = connection.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        ).fetchone()[0]

        rows.append(
            {
                "table_name": table_name,
                "row_count": row_count,
            }
        )

    return pd.DataFrame(rows)


def export_analytics_outputs(connection: duckdb.DuckDBPyConnection) -> None:
    """
    Export analytical summary tables as CSV files.
    """
    ANALYTICS_OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    analytics_tables = [
        "market_overview",
        "room_type_summary",
        "neighbourhood_summary",
        "host_portfolio_summary",
        "review_score_summary",
    ]

    for table_name in analytics_tables:
        output_path = ANALYTICS_OUTPUTS_DIR / f"{table_name}_from_src.csv"
        dataframe = connection.execute(f"SELECT * FROM {table_name}").fetchdf()
        dataframe.to_csv(output_path, index=False)


def run_duckdb_warehouse_builder() -> None:
    """
    Build DuckDB warehouse and export table summaries.
    """
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)
    DATA_QUALITY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    listing_master_path = get_listing_master_path()

    print(f"Using listing master: {listing_master_path}")
    print(f"Creating DuckDB warehouse: {DUCKDB_DATABASE_PATH}")

    connection = duckdb.connect(str(DUCKDB_DATABASE_PATH))

    print("Creating base listing master table...")
    create_base_table(connection, listing_master_path)

    print("Creating star schema tables...")
    create_star_schema(connection)

    print("Creating analytics summary tables...")
    create_analytics_tables(connection)

    print("Creating warehouse table summary...")
    table_summary = create_table_summary(connection)

    print("Exporting analytics outputs...")
    export_analytics_outputs(connection)

    table_summary_output_path = DATA_QUALITY_REPORTS_DIR / "warehouse_table_summary_from_src.csv"
    table_summary.to_csv(table_summary_output_path, index=False)

    print("\nWarehouse table summary:")
    print(table_summary)

    print("\nMarket overview:")
    print(connection.execute("SELECT * FROM market_overview").fetchdf())

    connection.close()

    print(f"\nWarehouse table summary saved to: {table_summary_output_path}")
    print("\nDuckDB warehouse build completed successfully.")


if __name__ == "__main__":
    run_duckdb_warehouse_builder()