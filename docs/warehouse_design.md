# Warehouse Design

## Project

Inside Airbnb Market Intelligence Platform — Data Engineering, Analytics & AI

## Warehouse Purpose

The DuckDB warehouse is designed to support analytical querying, business reporting, statistical analysis, and machine learning preparation for the Amsterdam Airbnb market.

The warehouse converts cleaned listing-level data into a structured analytical model with dimension tables, a fact table, and reusable summary tables.

## Warehouse Technology

This project uses DuckDB as the local analytical warehouse.

DuckDB was selected because it is lightweight, fast for analytical queries, works well with parquet files, and is suitable for local data engineering and analytics workflows.

## Warehouse Location

The generated DuckDB database is stored locally at:

```text
warehouse/airbnb_market.duckdb
```

The warehouse can be recreated by running:

```bash
python -m src.warehouse.duckdb_builder
```

or through the full pipeline:

```bash
python -m src.pipeline_runner
```

## Source Table

The warehouse is built from the final listing master table:

```text
data/processed/amsterdam/listing_master_final_from_src.parquet
```

This table combines:

- Cleaned summary listings
- Selected detailed listing features
- Calendar availability metrics
- Review activity metrics
- Host portfolio segments
- Availability segments
- Neighbourhood-level market metrics

## Star Schema Overview

```text
dim_listing
     |
     |
fact_listing_market ----- dim_host
     |
     |
dim_neighbourhood
```

## Table Grain

The main fact table is:

```text
fact_listing_market
```

The grain of the fact table is:

```text
One row per Airbnb listing
```

Each listing is linked to listing, host, and neighbourhood dimensions.

## Dimension Tables

### `dim_listing`

Contains descriptive listing attributes.

Main fields:

- `listing_key`
- `listing_id`
- `listing_name`
- `room_type`
- `property_type`
- `minimum_nights`
- `accommodates`
- `bathrooms`
- `bedrooms`
- `beds`
- `amenities_count`
- `has_valid_price`
- `has_valid_coordinates`
- `license`

Purpose:

```text
Allows analysis by listing characteristics such as room type, property type, capacity, and amenities.
```

### `dim_host`

Contains host-related information.

Main fields:

- `host_key`
- `host_id`
- `host_name`
- `host_since`
- `host_is_superhost`
- `host_identity_verified`
- `calculated_host_listings_count`
- `host_portfolio_segment`

Purpose:

```text
Allows analysis by host type, host portfolio size, and host verification status.
```

Special handling:

```text
Rows with missing host_id are assigned to an Unknown Host record with host_key = -1.
```

This keeps the fact table referentially consistent.

### `dim_neighbourhood`

Contains neighbourhood-level market context.

Main fields:

- `neighbourhood_key`
- `neighbourhood`
- `neighbourhood_group`
- `neighbourhood_listing_count`
- `neighbourhood_avg_price`
- `neighbourhood_median_price`
- `neighbourhood_avg_availability_rate`
- `neighbourhood_avg_occupancy_proxy`
- `neighbourhood_total_reviews`

Purpose:

```text
Allows analysis by Amsterdam neighbourhood and supports local market comparison.
```

## Fact Table

### `fact_listing_market`

Contains listing-level market performance measures.

Main fields:

- `fact_key`
- `listing_key`
- `host_key`
- `neighbourhood_key`
- `listing_id`
- `price_numeric`
- `calendar_days`
- `available_days`
- `unavailable_days`
- `availability_rate`
- `occupancy_proxy`
- `weekend_availability_rate`
- `weekday_availability_rate`
- `number_of_reviews`
- `reviews_per_month`
- `detailed_review_count`
- `unique_reviewer_count`
- `detailed_reviews_last_365d`
- `avg_reviews_per_year`
- `comment_coverage_rate`
- `review_scores_rating`
- `review_scores_cleanliness`
- `review_scores_location`
- `review_scores_value`
- `estimated_revenue_proxy`

Purpose:

```text
Supports market performance analysis by price, availability, review activity, review quality, host type, and neighbourhood.
```

## Analytical Summary Tables

The warehouse also creates reusable summary tables for reporting.

### `market_overview`

Provides one-row market-level KPIs.

Includes:

- Total listings
- Total known hosts
- Total neighbourhoods
- Average listing price
- Median listing price
- Average availability rate
- Average occupancy proxy
- Listings with and without reviews
- Total detailed reviews
- Average review score
- Total estimated revenue proxy
- Listings missing or invalid price

### `room_type_summary`

Summarizes market performance by room type.

Used to compare:

- Entire homes/apartments
- Private rooms
- Hotel rooms
- Shared rooms

### `neighbourhood_summary`

Summarizes market performance by neighbourhood.

Used to identify:

- High-supply neighbourhoods
- High-price neighbourhoods
- High occupancy proxy areas
- High estimated revenue proxy areas

### `host_portfolio_summary`

Summarizes listings by host portfolio segment.

Segments include:

- Single-listing Host
- Small Portfolio Host
- Medium Portfolio Host
- Large Portfolio Host
- Unknown Host

### `review_score_summary`

Summarizes listings by review score band.

Bands include:

- Excellent
- Very good
- Good
- Below 4.0
- No rating

## Important Metrics

### Availability Rate

```text
available_days / calendar_days
```

Shows the proportion of calendar days where a listing is marked available.

### Occupancy Proxy

```text
unavailable_days / calendar_days
```

This is used as a proxy for occupancy.

Important limitation:

```text
Unavailable days may include both booked days and host-blocked days.
Therefore, occupancy_proxy is not the same as confirmed occupancy.
```

### Estimated Revenue Proxy

```text
price_numeric × unavailable_days
```

Important limitation:

```text
This is not actual revenue.
It is an estimated proxy because the calendar file does not include confirmed booking revenue.
```

### Calendar Limitation

The Amsterdam calendar file used in this project does not contain daily price or adjusted price columns.

Therefore:

```text
Calendar data is used for availability and stay-policy analysis, not actual daily price or revenue analysis.
```

## Warehouse Validation

The warehouse builder creates a row-count summary file:

```text
reports/data_quality/warehouse_table_summary_from_src.csv
```

Expected key table counts:

```text
listing_master_final       10,465
fact_listing_market        10,465
dim_listing                10,465
dim_host                   around 9,105
dim_neighbourhood          22
market_overview            1
room_type_summary          4
neighbourhood_summary      22
host_portfolio_summary     around 5
review_score_summary       around 5
```

## SQL Files

Warehouse schema documentation is stored in:

```text
sql/ddl/
```

Analytical SQL queries are stored in:

```text
sql/analysis_queries/
```

## Design Strengths

This warehouse design supports:

- Clear separation between dimensions and facts
- Reusable analytical summary tables
- SQL-based reporting
- Business-friendly analysis by room type, host segment, neighbourhood, and review score
- Reproducible warehouse creation from Python scripts
- Integration with downstream EDA, statistical analysis, ML, and dashboards

## Design Limitations

The warehouse has the following limitations:

- It uses one city snapshot only.
- Calendar data does not include actual booking confirmation.
- Estimated revenue is a proxy, not real revenue.
- Missing prices reduce coverage for price and ML analysis.
- Some property types and room types have small sample sizes.
- Neighbourhood-level price features should be handled carefully in strict ML settings to avoid target-derived leakage.

## Reproducibility

The warehouse can be rebuilt from processed data using:

```bash
python -m src.warehouse.duckdb_builder
```

The full processed data and warehouse pipeline can be recreated using:

```bash
python -m src.pipeline_runner
```
