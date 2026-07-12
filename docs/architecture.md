# Project Architecture

## Project Name

Inside Airbnb Market Intelligence Platform — Data Engineering, Analytics & AI

## Purpose

This project builds an end-to-end market intelligence platform using Inside Airbnb data for Amsterdam.

The goal is to transform raw Airbnb datasets into a clean analytical warehouse, generate business insights, perform statistical analysis, and train a machine learning model for price prediction.

## High-Level Architecture

```text
Raw Inside Airbnb Data
        |
        v
Data Ingestion
        |
        v
Dataset Profiling and Data Quality Validation
        |
        v
Cleaning and Aggregation
        |
        v
Final Listing Master Table
        |
        v
DuckDB Analytical Warehouse
        |
        v
EDA, SQL Analytics, Statistical Analysis, and Machine Learning
        |
        v
Reports, Figures, Model Outputs, and Business Insights
```

Repository Architecture

```
data/
├── raw/
├── interim/
├── processed/
└── external/

notebooks/
├── 01_dataset_familiarization.ipynb
├── 02_duckdb_warehouse.ipynb
├── 03_eda_business_analysis.ipynb
├── 04_statistical_analysis.ipynb
└── 05_ml_price_prediction.ipynb

src/
├── config.py
├── pipeline_runner.py
├── ingestion/
├── profiling/
├── validation/
├── cleaning/
├── transformation/
├── warehouse/
├── ml/
└── utils/

sql/
├── analysis_queries/
└── ddl/

reports/
├── data_quality/
├── analytics_outputs/
├── statistical_analysis/
├── machine_learning/
└── figures/

models/
warehouse/
docs/
```

## Pipeline Stages

1. Ingestion

The ingestion layer checks whether all expected raw files are available and loads the tabular datasets.

Main script:

```bash
python -m src.ingestion.raw_data_loader
```

2. Profiling

The profiling layer creates dataset inventory, schema profile, and missing value reports.

Main script:

```bash
python -m src.profiling.dataset_profiler
```

3. Validation

The validation layer checks important data quality rules, including missing IDs, duplicate IDs, invalid prices, invalid coordinates, calendar validity, relationship coverage, and neighbourhood lookup coverage.

Main script:

```bash
python -m src.validation.data_quality_checks
```

4. Cleaning and Aggregation

The cleaning layer prepares reusable processed outputs:

- Cleaned summary listings
- Calendar listing-level availability metrics
- Review listing-level activity metrics

Main scripts:

```bash
python -m src.cleaning.listings_cleaner
python -m src.cleaning.calendar_cleaner
python -m src.cleaning.reviews_cleaner
```

5. Transformation

The transformation layer builds the final listing master table by combining cleaned listings, detailed listing attributes, calendar metrics, review metrics, host segments, availability segments, and neighbourhood metrics.

Main script:

```bash
python -m src.transformation.listing_master_builder
```

6. Warehouse

The warehouse layer creates a DuckDB analytical warehouse with a star schema and reusable summary tables.

Main script:

```bash
python -m src.warehouse.duckdb_builder
```

7. Machine Learning

The ML layer trains price prediction models and saves model comparison, feature importance, residual analysis, and final model artifacts.

Main script:

```bash
python -m src.ml.train_price_model
```

## Full Pipeline Execution

The full reusable pipeline can be executed using:

```bash
python -m src.pipeline_runner
```

The ML training workflow can be executed separately using:

```bash
python -m src.ml.train_price_model
```

## Key Design Decisions

### Summary listings as base table

The summary listings dataset is used as the base listing universe because it provides the broadest listing coverage.

### Calendar limitation

The Amsterdam calendar file does not contain daily price or adjusted price fields. Therefore, calendar data is used for availability and occupancy proxy metrics, not actual daily revenue.

### Occupancy proxy

Occupancy proxy is calculated using unavailable days. This is not the same as confirmed bookings because unavailable dates may include both booked and host-blocked dates.

### Estimated revenue proxy

Estimated revenue proxy is calculated as:

```text
price_numeric × unavailable_days
```

This is only a proxy and is not treated as actual revenue.

### Target leakage control

Estimated revenue proxy is excluded from machine learning because it directly uses price and would create target leakage.

## Final Outputs

The project produces:

- Data quality reports
- Cleaned processed datasets
- Final listing master table
- DuckDB analytical warehouse
- SQL analytics outputs
- EDA figures
- Statistical test outputs
- Machine learning model comparison
- Random Forest feature importance
- Prediction error and residual analysis
- Final model artifact

## Reproducibility

The project is designed to be reproducible using reusable Python scripts under `src/`.

Generated datasets, model artifacts, and warehouse files are not committed to Git because they can be recreated by running the pipeline.
