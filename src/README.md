# Source Code

This folder contains reusable Python modules for the Inside Airbnb Market Intelligence Platform.

The notebooks are used for exploration, explanation, and reporting.  
The `src` folder is used to organize reusable pipeline logic for profiling, cleaning, validation, transformation, warehouse creation, and machine learning.

## Planned Modules

- `config.py`  
  Central project paths and settings.

- `ingestion/`  
  Raw data loading and file checks.
### `ingestion/raw_data_loader.py`

Checks whether all expected raw Inside Airbnb files are available and loads the tabular CSV/CSV.GZ datasets into pandas DataFrames.

Run from project root:

```bash
python -m src.ingestion.raw_data_loader

- `profiling/`  
  Dataset inventory and schema profiling.
### `profiling/dataset_profiler.py`

Creates reusable dataset inventory, schema profile, and missing value summary reports.

Run from project root:

```bash
python -m src.profiling.dataset_profiler

- `cleaning/`  
  Cleaning functions for listings, calendar, and reviews.
### `cleaning/listings_cleaner.py`

Cleans the raw summary listings dataset.

Main outputs:
- Standardized `listing_id`
- Numeric `price_numeric`
- Parsed review date
- Cleaned text columns
- Data quality flags for price, coordinates, and reviews
- Processed listings parquet output
- Cleaning summary report

Run from project root:

```bash
python -m src.cleaning.listings_cleaner

### `cleaning/calendar_cleaner.py`

Cleans and aggregates the raw calendar dataset into listing-level availability metrics.

Main outputs:
- Calendar day count per listing
- Available and unavailable day counts
- Availability rate
- Occupancy proxy
- Weekend availability rate
- Weekday availability rate
- Minimum and maximum night policy metrics

Important limitation: the Amsterdam calendar file used in this project does not include daily price or adjusted price columns, so this script does not calculate daily calendar revenue.

Run from project root:

```bash
python -m src.cleaning.calendar_cleaner

### `cleaning/reviews_cleaner.py`

Cleans and aggregates the raw detailed reviews dataset into listing-level review activity metrics.

Main outputs:
- Detailed review count
- Unique reviewer count
- First and last review date
- Reviews in the last 365 days
- Comment coverage rate
- Average and median comment length
- Average reviews per year

Run from project root:

```bash
python -m src.cleaning.reviews_cleaner

- `validation/`  
  Data quality and relationship validation checks.
  ### `validation/data_quality_checks.py`

Runs reusable data quality checks across the raw Inside Airbnb datasets.

Checks include:
- Missing and duplicate listing IDs
- Missing and invalid prices
- Invalid coordinates
- Calendar availability validity
- Duplicate listing-date calendar rows
- Review ID uniqueness
- Relationship coverage between listing, calendar, and review datasets
- Neighbourhood lookup coverage

Run from project root:

```bash
python -m src.validation.data_quality_checks


- `transformation/`  
  Feature engineering and final listing master creation.
  ### `transformation/listing_master_builder.py`

Builds the final analytical listing master table by combining:
- Cleaned summary listings
- Selected detailed listing features
- Calendar availability metrics
- Review activity metrics
- Neighbourhood-level market metrics

Main outputs:
- `data/processed/amsterdam/listing_master_final_from_src.parquet`
- `reports/data_quality/listing_master_summary_from_src.csv`

Run from project root:

```bash
python -m src.transformation.listing_master_builder


- `warehouse/`  
  DuckDB warehouse and star schema creation.
  ### `warehouse/duckdb_builder.py`

Builds the DuckDB analytical warehouse from the final listing master table.

Main outputs:
- `warehouse/airbnb_market.duckdb`
- `listing_master_final`
- `dim_listing`
- `dim_host`
- `dim_neighbourhood`
- `fact_listing_market`
- Reusable analytical summary tables
- Exported analytics CSV outputs

Run from project root:

```bash
python -m src.warehouse.duckdb_builder


- `ml/`  
  Machine learning dataset preparation, training, and evaluation.
### `ml/train_price_model.py`

Trains reusable machine learning models for Airbnb price prediction.

Main steps:
- Loads the final listing master table
- Prepares numeric and categorical features
- Excludes target leakage fields
- Trains baseline, linear, ridge, random forest, and gradient boosting models
- Compares model performance using MAE, RMSE, and R²
- Saves the final Random Forest model package
- Saves feature importance and residual analysis outputs

Run from project root:

```bash
python -m src.ml.train_price_model

- `utils/`  
  Shared helper functions.

  ## Full Pipeline Runner

The full reusable pipeline can be executed from the project root:

```bash
python -m src.pipeline_runner