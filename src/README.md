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

- `validation/`  
  Data quality and relationship validation checks.

- `transformation/`  
  Feature engineering and final listing master creation.

- `warehouse/`  
  DuckDB warehouse and star schema creation.

- `ml/`  
  Machine learning dataset preparation, training, and evaluation.

- `utils/`  
  Shared helper functions.