# Inside Airbnb Market Intelligence Platform  
## Data Engineering, Analytics & AI Project

## 1. Project Overview

This project builds an end-to-end Airbnb market intelligence platform using Inside Airbnb data for Amsterdam.

The goal is to transform raw Airbnb datasets into a clean analytical warehouse, generate business insights, perform statistical analysis, and build a machine learning model for price prediction.

The project covers the full workflow from raw data ingestion to business reporting and machine learning explainability.

---

## 2. Business Problem

Airbnb market data contains valuable information about listing supply, pricing, availability, reviews, host behavior, and neighbourhood performance.

However, the raw datasets are large, messy, and spread across multiple files.

This project answers questions such as:

- Which room types dominate the Amsterdam Airbnb market?
- Which neighbourhoods show stronger market activity?
- How do price, availability, reviews, and host type vary across the market?
- Which factors are associated with listing price?
- Can machine learning estimate Airbnb listing prices?
- Where does the price prediction model perform well or struggle?
- How can this platform be extended with AI-powered market intelligence?

---

## 3. Assignment Competencies Covered

This project was designed to demonstrate the following competencies:

| Competency | Project Coverage |
|---|---|
| Data Engineering Fundamentals | Ingestion, profiling, cleaning, validation, warehouse, pipeline |
| Analytical Thinking | EDA, SQL analytics, business interpretation |
| Statistical Reasoning | Hypothesis testing, effect sizes, correlation analysis |
| Data Science & ML | Feature engineering, model training, validation, explainability |
| AI & LLM Literacy | Responsible AI usage documentation and open innovation concept |
| Communication & Storytelling | Business-focused insights, documentation, reports |
| Creativity & Initiative | End-to-end platform, DuckDB warehouse, ML, AI assistant concept |
| Professionalism | Modular code, reproducibility, structured repository |

---

## 4. Dataset

The project uses Inside Airbnb data for:

```text
Amsterdam, North Holland, The Netherlands
Snapshot date: 2026-06-15
```

Expected raw files:

```text
data/raw/amsterdam/2026-06-15/
├── listings.csv.gz
├── calendar.csv.gz
├── reviews.csv.gz
├── listings.csv
├── reviews.csv
├── neighbourhoods.csv
└── neighbourhoods.geojson
```

Main datasets used:

| Dataset | Purpose |
|---|---|
| `listings.csv` | Summary listing information |
| `listings.csv.gz` | Detailed listing attributes |
| `calendar.csv.gz` | Availability and stay-policy analysis |
| `reviews.csv.gz` | Detailed review activity metrics |
| `reviews.csv` | Summary review dates |
| `neighbourhoods.csv` | Neighbourhood lookup |
| `neighbourhoods.geojson` | Geospatial reference |

Important calendar limitation:

```text
The Amsterdam calendar file used in this project does not contain daily price or adjusted_price columns.
Therefore, calendar data is used for availability and occupancy proxy analysis, not actual daily revenue analysis.
```

---

## 5. High-Level Architecture

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

---

## 6. Repository Structure

```text
.
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   ├── external/
│   └── README.md
│
├── docs/
│   ├── architecture.md
│   ├── warehouse_design.md
│   ├── model_card.md
│   ├── rubric_alignment.md
│   ├── ai_llm_usage_and_open_innovation.md
│   ├── project_plan.md
│   ├── project_tracker.md
│   └── data_dictionary_notes.md
│
├── notebooks/
│   ├── 01_dataset_familiarization.ipynb
│   ├── 02_duckdb_warehouse.ipynb
│   ├── 03_eda_business_analysis.ipynb
│   ├── 04_statistical_analysis.ipynb
│   └── 05_ml_price_prediction.ipynb
│
├── reports/
│   ├── data_quality/
│   ├── analytics_outputs/
│   ├── statistical_analysis/
│   ├── machine_learning/
│   ├── figures/
│   ├── ai_usage_disclosure.md
│   ├── assumptions_log.md
│   └── decision_log.md
│
├── sql/
│   ├── analysis_queries/
│   └── ddl/
│
├── src/
│   ├── config.py
│   ├── pipeline_runner.py
│   ├── ingestion/
│   ├── profiling/
│   ├── validation/
│   ├── cleaning/
│   ├── transformation/
│   ├── warehouse/
│   ├── ml/
│   └── utils/
│
├── models/
│   └── README.md
│
├── warehouse/
│   └── README.md
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 7. Reusable Pipeline

The project includes reusable Python modules under `src/`.

### Main pipeline command

```bash
python -m src.pipeline_runner
```

This runs:

1. Project directory setup  
2. Raw data file checks  
3. Dataset profiling  
4. Data quality validation  
5. Summary listings cleaning  
6. Calendar cleaning and aggregation  
7. Reviews cleaning and aggregation  
8. Final listing master build  
9. DuckDB warehouse build  

### Machine learning training command

```bash
python -m src.ml.train_price_model
```

This trains price prediction models and saves:

- Model comparison results
- Final ML summary
- Random Forest feature importance
- Prediction results
- Residual summary
- Diagnostic plots
- Final model package

---

## 8. Setup Instructions

### 8.1 Create virtual environment

```bash
python -m venv .venv
```

### 8.2 Activate virtual environment on Windows

```bash
.venv\Scripts\activate
```

### 8.3 Install dependencies

```bash
pip install -r requirements.txt
```

### 8.4 Add raw data files

Place the Inside Airbnb Amsterdam files in:

```text
data/raw/amsterdam/2026-06-15/
```

### 8.5 Run the full pipeline

```bash
python -m src.pipeline_runner
```

### 8.6 Run ML training

```bash
python -m src.ml.train_price_model
```

---

## 9. Data Engineering Outputs

The project generates data quality and processed outputs such as:

```text
reports/data_quality/
├── dataset inventory reports
├── schema profile reports
├── missing value summaries
├── validation reports
├── cleaning summaries
├── listing master summary
└── warehouse table summary
```

Processed files are generated under:

```text
data/processed/amsterdam/
```

Important processed outputs include:

- Cleaned summary listings
- Calendar listing-level metrics
- Review listing-level metrics
- Final listing master table

Generated processed datasets are not committed to Git because they can be recreated by running the pipeline.

---

## 10. DuckDB Warehouse

The project builds a local DuckDB analytical warehouse.

Warehouse file:

```text
warehouse/airbnb_market.duckdb
```

The warehouse includes:

### Dimension tables

- `dim_listing`
- `dim_host`
- `dim_neighbourhood`

### Fact table

- `fact_listing_market`

### Analytical summary tables

- `market_overview`
- `room_type_summary`
- `neighbourhood_summary`
- `host_portfolio_summary`
- `review_score_summary`

Warehouse design documentation:

```text
docs/warehouse_design.md
```

DDL documentation:

```text
sql/ddl/
```

---

## 11. Analytical SQL

Reusable SQL queries are stored in:

```text
sql/analysis_queries/
```

Queries include:

- Market overview
- Room type summary
- Neighbourhood summary
- Host portfolio summary
- Review score summary
- Top neighbourhood-room type revenue proxy analysis

---

## 12. Exploratory Data Analysis

EDA is performed in:

```text
notebooks/03_eda_business_analysis.ipynb
```

Main analysis areas:

- Market overview
- Room type performance
- Neighbourhood performance
- Host portfolio analysis
- Review score analysis
- Price distribution and outliers
- Availability and occupancy proxy analysis
- Correlation analysis

Example insights:

- Entire homes/apartments dominate Amsterdam Airbnb supply.
- Price is right-skewed, so median price is more reliable than mean price.
- Neighbourhoods vary strongly in listing supply, price, and estimated revenue proxy.
- Review scores are concentrated near the high end, suggesting review score inflation.
- Availability and occupancy proxy should be interpreted carefully because unavailable days may include host-blocked dates.

---

## 13. Statistical Analysis

Statistical analysis is performed in:

```text
notebooks/04_statistical_analysis.ipynb
```

Methods used:

- Kruskal-Wallis tests
- Mann-Whitney U pairwise comparisons
- Bonferroni correction
- Effect size interpretation
- Spearman correlation analysis

Main statistical questions:

- Do prices differ significantly by room type?
- Do prices differ by host portfolio segment?
- Does occupancy proxy differ by room type?
- Do review scores differ by room type?
- Which numeric features are significantly associated with price?

Statistical outputs are saved in:

```text
reports/statistical_analysis/
```

---

## 14. Machine Learning

Machine learning is performed in:

```text
notebooks/05_ml_price_prediction.ipynb
src/ml/train_price_model.py
```

### Problem type

```text
Supervised regression
```

### Target

```text
price_numeric
```

### Rows used

```text
6,471 listings with valid positive price values
```

### Models compared

- Dummy Median Baseline
- Linear Regression
- Ridge Regression
- Random Forest Regressor
- Gradient Boosting Regressor

### Final selected model

```text
Random Forest Regressor
```

### Final performance

| Metric | Value |
|---|---:|
| MAE | 88.40 |
| RMSE | 147.30 |
| R² Score | 0.5009 |

### Baseline comparison

| Metric | Value |
|---|---:|
| Dummy Median Baseline RMSE | 213.50 |
| RMSE Improvement | 66.20 |
| RMSE Improvement Percentage | 31.01% |

### Model explainability

Feature importance analysis shows that important predictive signals include:

- Bedrooms
- Review scores value
- Minimum nights
- Beds
- Bathrooms
- Neighbourhood context
- Amenities count
- Reviews per month
- Accommodates
- Room type
- Availability and occupancy proxy

Model card:

```text
docs/model_card.md
```

---

## 15. Important Assumptions and Limitations

### Occupancy proxy

```text
occupancy_proxy = unavailable_days / calendar_days
```

This is not confirmed occupancy. Unavailable days may include booked dates or dates blocked by the host.

### Estimated revenue proxy

```text
estimated_revenue_proxy = price_numeric × unavailable_days
```

This is not actual revenue. It is only a proxy because actual booking revenue is not available.

### Missing prices

Some listings have missing or invalid price values. These listings are excluded from price-based ML training.

### One-city snapshot

The project currently focuses on one Amsterdam snapshot. Results may not generalize to other cities or time periods.

### ML limitations

The model does not include photos, interior quality, exact view, street-level desirability, events, seasonality, or confirmed booking data.

---

## 16. AI / LLM Usage and Open Innovation

AI tools were used responsibly as support for planning, debugging, learning, documentation, and interpretation.

AI-generated suggestions were reviewed and validated using actual dataset outputs, notebook results, terminal outputs, and generated reports.

AI usage documentation:

```text
reports/ai_usage_disclosure.md
docs/ai_llm_usage_and_open_innovation.md
```

### Open innovation concept

A future extension is an AI-powered Airbnb Market Intelligence Assistant.

This assistant could help users ask natural language questions such as:

- Which neighbourhoods have the highest estimated revenue proxy?
- Which features influence price prediction?
- Why does the model struggle with some luxury listings?
- Which room types perform best?
- What are the risks of interpreting occupancy proxy as real occupancy?

The assistant would use the DuckDB warehouse, reports, ML outputs, and guardrails to provide grounded business explanations.

---

## 17. Key Documentation

| Document | Purpose |
|---|---|
| `docs/architecture.md` | End-to-end project architecture |
| `docs/warehouse_design.md` | DuckDB warehouse and star schema design |
| `docs/model_card.md` | ML model purpose, performance, limitations |
| `docs/rubric_alignment.md` | Mapping project work to assignment criteria |
| `docs/ai_llm_usage_and_open_innovation.md` | Responsible AI use and future AI concept |
| `reports/assumptions_log.md` | Project assumptions |
| `reports/decision_log.md` | Major design decisions |
| `reports/ai_usage_disclosure.md` | AI usage disclosure |

---

## 18. Generated Artifacts

Generated artifacts include:

- Data quality reports
- Analytical output CSVs
- Statistical test results
- EDA figures
- ML evaluation reports
- Feature importance reports
- Residual analysis reports
- DuckDB warehouse
- ML model package

Large generated files such as raw data, processed parquet files, DuckDB databases, and model artifacts are not committed to Git. They can be recreated using the provided pipeline commands.

---

## 19. Project Status

Completed:

- Dataset familiarization
- Data profiling
- Data quality validation
- Data cleaning
- Feature engineering
- Final listing master creation
- DuckDB warehouse
- Star schema
- SQL analytics
- EDA
- Statistical analysis
- ML price prediction
- Feature importance
- Residual analysis
- Reusable Python pipeline
- DDL documentation
- Model card
- Rubric alignment
- AI usage and open innovation documentation

Remaining possible improvements:

- Add Power BI or Streamlit dashboard
- Add final presentation slides
- Extend analysis to multiple cities
- Add natural language AI assistant prototype
- Add automated tests
- Add CI/CD workflow

---

## 20. Final Project Summary

This project demonstrates an end-to-end data workflow using real-world Airbnb market data.

It combines data engineering, analytics, statistics, machine learning, responsible AI documentation, and professional repository structure.

The result is a reproducible market intelligence platform that can support business understanding of Airbnb supply, pricing, availability, reviews, host behavior, and neighbourhood performance.