# Final Report  
# Inside Airbnb Market Intelligence Platform  
## Data Engineering, Analytics & AI Project

---

## 1. Executive Summary

This project builds an end-to-end Airbnb market intelligence platform using Inside Airbnb data for Amsterdam, North Holland, The Netherlands.

The project transforms raw Airbnb datasets into cleaned analytical datasets, validates data quality, builds a DuckDB warehouse, performs exploratory and statistical analysis, and trains a machine learning model to predict listing prices.

The final solution demonstrates data engineering, analytics, statistical reasoning, machine learning, responsible AI usage, and professional project documentation.

Key outcomes:

- Built a reusable data pipeline under `src/`
- Created data quality validation reports
- Built a final listing master dataset
- Built a DuckDB analytical warehouse with star schema design
- Created SQL analytical summary tables
- Completed EDA and business analysis
- Completed statistical testing with effect size interpretation
- Trained and evaluated multiple ML models for price prediction
- Selected Random Forest as the final model
- Documented AI usage, assumptions, limitations, and open innovation opportunities

---

## 2. Project Objective

The objective of this project is to convert raw Airbnb market data into a structured market intelligence platform.

The platform aims to answer business questions such as:

- Which room types dominate the Amsterdam Airbnb market?
- Which neighbourhoods show stronger market activity?
- How do prices vary by room type, host type, and neighbourhood?
- What features are associated with listing price?
- Can machine learning estimate Airbnb listing prices?
- Where does the model perform well or struggle?
- How can AI be used to make market intelligence easier for business users?

---

## 3. Dataset Overview

The project uses Inside Airbnb data for:

```text
City: Amsterdam, North Holland, The Netherlands
Snapshot date: 2026-06-15
```

Raw files used:

```text
listings.csv.gz
calendar.csv.gz
reviews.csv.gz
listings.csv
reviews.csv
neighbourhoods.csv
neighbourhoods.geojson
```

Main dataset roles:

| Dataset | Purpose |
|---|---|
| `listings.csv` | Summary listing information |
| `listings.csv.gz` | Detailed listing attributes |
| `calendar.csv.gz` | Availability and stay-policy metrics |
| `reviews.csv.gz` | Detailed review activity |
| `reviews.csv` | Summary review dates |
| `neighbourhoods.csv` | Neighbourhood lookup |
| `neighbourhoods.geojson` | Geospatial reference |

Important dataset limitation:

The Amsterdam calendar file does not contain daily price or adjusted price fields. Therefore, calendar data is used for availability and occupancy proxy analysis, not actual daily revenue analysis.

---

## 4. Project Architecture

The project follows this architecture:

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

The reusable pipeline can be executed using:

```bash
python -m src.pipeline_runner
```

The machine learning workflow can be executed using:

```bash
python -m src.ml.train_price_model
```

---

## 5. Data Engineering Work

The data engineering workflow includes:

- Raw file validation
- Dataset inventory generation
- Schema profiling
- Missing value profiling
- Data quality checks
- Listings cleaning
- Calendar cleaning and aggregation
- Reviews cleaning and aggregation
- Final listing master creation
- DuckDB warehouse build
- Star schema design
- Reusable pipeline runner

Main reusable scripts:

```text
src/ingestion/raw_data_loader.py
src/profiling/dataset_profiler.py
src/validation/data_quality_checks.py
src/cleaning/listings_cleaner.py
src/cleaning/calendar_cleaner.py
src/cleaning/reviews_cleaner.py
src/transformation/listing_master_builder.py
src/warehouse/duckdb_builder.py
src/ml/train_price_model.py
src/pipeline_runner.py
```

This improves reproducibility because the project is not only notebook-based. The key workflow can be rerun through scripts.

---

## 6. Data Quality Validation

The project validates important data quality rules, including:

- Missing listing IDs
- Duplicate listing IDs
- Missing and invalid prices
- Invalid latitude and longitude values
- Calendar availability values
- Duplicate listing-date calendar rows
- Review ID uniqueness
- Relationship coverage between listings, calendar, and reviews
- Neighbourhood lookup coverage

Important quality findings:

- Summary listings contain 10,465 unique listing rows.
- The calendar file contains 3,819,725 rows.
- The detailed reviews file contains 545,162 rows.
- 3,994 listings have missing or invalid price values.
- 6,471 listings have valid positive prices for ML.
- Neighbourhood coverage is complete for the Amsterdam neighbourhood lookup.

---

## 7. Final Listing Master

The final listing master combines:

- Cleaned summary listings
- Detailed listing features
- Calendar availability metrics
- Review activity metrics
- Host portfolio segments
- Availability segments
- Neighbourhood-level market metrics

Expected final listing master summary:

| Metric | Value |
|---|---:|
| Listing rows | 10,465 |
| Unique listing IDs | 10,465 |
| Valid price rows | 6,471 |
| Missing or invalid price rows | 3,994 |
| Listings with calendar metrics | 10,465 |
| Listings with review metrics | Around 9,432 |
| Neighbourhood count | 22 |

---

## 8. Warehouse Design

The project uses DuckDB as the analytical warehouse.

Warehouse file:

```text
warehouse/airbnb_market.duckdb
```

The warehouse includes a star schema.

Dimension tables:

```text
dim_listing
dim_host
dim_neighbourhood
```

Fact table:

```text
fact_listing_market
```

Analytical summary tables:

```text
market_overview
room_type_summary
neighbourhood_summary
host_portfolio_summary
review_score_summary
```

The fact table grain is:

```text
One row per Airbnb listing
```

The warehouse supports business analysis by room type, host segment, neighbourhood, review score, price, availability, occupancy proxy, and estimated revenue proxy.

---

## 9. Key Metrics

### Availability Rate

```text
availability_rate = available_days / calendar_days
```

This measures the proportion of calendar days where a listing is marked available.

### Occupancy Proxy

```text
occupancy_proxy = unavailable_days / calendar_days
```

This is only a proxy. Unavailable days may include booked dates or dates blocked by the host.

### Estimated Revenue Proxy

```text
estimated_revenue_proxy = price_numeric × unavailable_days
```

This is not actual revenue. It is an estimated proxy because confirmed booking revenue is not available.

---

## 10. Exploratory Data Analysis

EDA was performed to understand Airbnb market structure and business patterns.

Main EDA areas:

- Market overview
- Room type analysis
- Neighbourhood analysis
- Host portfolio analysis
- Review score analysis
- Price distribution
- Availability and occupancy proxy
- Correlation analysis

Key findings:

- Entire homes/apartments dominate Amsterdam Airbnb supply.
- Price is strongly right-skewed, so median price is more reliable than average price.
- Neighbourhoods show strong differences in supply, price, review activity, and estimated revenue proxy.
- Review scores are concentrated near the high end, suggesting review score inflation.
- High-price listings and unusual properties create more prediction difficulty later in ML.
- Availability and occupancy proxy should be interpreted carefully because unavailable days are not confirmed bookings.

---

## 11. Statistical Analysis

The project used non-parametric statistical methods because Airbnb price and review score distributions are skewed and contain outliers.

Methods used:

- Kruskal-Wallis test
- Mann-Whitney U pairwise comparisons
- Bonferroni correction
- Effect size interpretation
- Spearman correlation analysis

Statistical questions tested:

- Do prices differ significantly by room type?
- Do prices differ by host portfolio segment?
- Does occupancy proxy differ by room type?
- Do review scores differ by room type?
- Which numeric features are associated with price?

Important findings:

- Room type price differences are statistically significant.
- Host portfolio segment price differences are statistically significant.
- Occupancy proxy differs by room type.
- Review score distributions differ by room type.
- Property size features such as bedrooms, beds, bathrooms, and accommodates are meaningfully associated with price.
- Availability rate and occupancy proxy have weaker direct correlation with price.

The statistical work confirms that several EDA patterns are not only visual patterns but are supported by statistical testing.

---

## 12. Machine Learning

The project builds a supervised regression model to estimate Airbnb listing price.

Target variable:

```text
price_numeric
```

Rows used for ML:

```text
6,471 listings with valid positive prices
```

Train/test split:

```text
80% training
20% testing
```

Models compared:

- Dummy Median Baseline
- Linear Regression
- Ridge Regression
- Random Forest Regressor
- Gradient Boosting Regressor

Final selected model:

```text
Random Forest Regressor
```

Final model performance:

| Metric | Value |
|---|---:|
| MAE | 88.40 |
| RMSE | 147.30 |
| R² Score | 0.5009 |

Baseline comparison:

| Metric | Value |
|---|---:|
| Dummy Median Baseline RMSE | 213.50 |
| RMSE Improvement | 66.20 |
| RMSE Improvement Percentage | 31.01% |

The Random Forest model reduced RMSE by 31.01% compared with the dummy baseline.

This shows that listing, host, review, availability, and neighbourhood features contain useful signals for price prediction.

---

## 13. Model Explainability

Feature importance analysis shows that the model uses these features strongly:

- Bedrooms
- Review scores value
- Minimum nights
- Beds
- Bathrooms
- Neighbourhood context
- Average reviews per year
- Amenities count
- Reviews per month
- Accommodates
- Room type
- Availability and occupancy proxy

Important interpretation:

Feature importance shows predictive value, not causation.

For example, bedrooms are a strong predictive signal for price, but this does not mean bedrooms alone cause price changes.

---

## 14. Residual and Error Analysis

Residual analysis was used to understand where the model makes mistakes.

Residual summary:

| Metric | Value |
|---|---:|
| Mean Error | -9.84 |
| Median Error | -19.76 |
| Mean Absolute Error | 88.40 |
| Median Absolute Error | 58.41 |
| Maximum Absolute Error | 1578.65 |
| Prediction Count | 1,295 |

The negative mean error shows that the model slightly overpredicts on average.

Large errors are mostly found in unusual or premium listings, such as:

- Luxury houseboats
- Historical sailing ships
- Canal-view properties
- High-end townhouses
- Unique premium properties

This is expected because the dataset does not fully capture photos, interior quality, exact view, luxury design, or street-level desirability.

---

## 15. AI / LLM Usage

AI tools were used responsibly as support during the project.

AI assistance was used for:

- Project planning
- Debugging
- Explaining technical concepts
- Improving documentation
- Interpreting statistical and ML outputs
- Designing reusable pipeline structure
- Preparing report and README content

AI was not used to fabricate results.

All important outputs were checked against:

- Actual dataset schemas
- Notebook outputs
- Terminal outputs
- Generated CSV reports
- Model metrics
- Feature importance outputs
- Residual analysis outputs

The project follows a human-in-the-loop approach.

---

## 16. Open Innovation Concept

A future extension of this project is an:

```text
AI-powered Airbnb Market Intelligence Assistant
```

This assistant could allow business users to ask natural language questions such as:

- Which neighbourhoods have the highest estimated revenue proxy?
- Which room types perform best?
- Why is a listing predicted to be expensive?
- Which features influence price?
- Where does the model struggle?
- What are the risks of interpreting occupancy proxy?

The assistant could use:

- DuckDB warehouse
- SQL query templates
- Generated reports
- ML outputs
- LLM-based explanation generation
- Guardrails for proxy metrics and limitations

Important guardrails:

- Do not treat estimated revenue proxy as actual revenue.
- Do not treat occupancy proxy as confirmed occupancy.
- Do not make unsupported claims about hosts or guests.
- Always mention limitations when using proxy metrics.
- Use database outputs instead of guessing.

---

## 17. Key Assumptions

Important project assumptions:

- Summary listings are used as the base listing universe.
- Calendar unavailable days are used as an occupancy proxy.
- Estimated revenue proxy is not actual revenue.
- Missing prices reduce price analysis and ML coverage.
- Neighbourhood metrics are useful for market context.
- One snapshot is not enough to make time-series conclusions.
- ML predictions are approximate and not final pricing recommendations.

---

## 18. Key Limitations

This project has the following limitations:

- Only one city snapshot is analyzed.
- Calendar data does not include confirmed bookings.
- Calendar data does not include daily price fields.
- Estimated revenue proxy is not actual revenue.
- Some listings have missing prices.
- ML does not include photos, interior quality, exact view, events, or seasonality.
- Some small room type groups have limited sample sizes.
- Results may not generalize to other cities or future dates.

---

## 19. Business Value

This project provides business value by turning raw Airbnb data into structured market intelligence.

Potential users could include:

- Data analysts
- Market researchers
- Property investors
- Tourism analysts
- Hosts
- Business intelligence teams

The platform helps users understand:

- Market supply
- Price patterns
- Neighbourhood performance
- Host behavior
- Review activity
- Availability behavior
- Price prediction drivers
- Model limitations

---

## 20. Professionalism and Reproducibility

The repository is structured professionally with:

- Modular source code
- Reusable pipeline runner
- Data documentation
- Warehouse documentation
- Model card
- Rubric alignment
- AI usage disclosure
- Assumption and decision logs
- `.gitignore` for large generated files
- Clear setup and run instructions

Reproducibility commands:

```bash
python -m src.pipeline_runner
```

```bash
python -m src.ml.train_price_model
```

Generated artifacts such as raw data, processed parquet files, DuckDB database files, and model files are not committed to Git because they can be recreated.

---

## 21. Rubric Coverage Summary

| Competency | Coverage |
|---|---|
| Data Engineering Fundamentals | Strong |
| Analytical Thinking | Strong |
| Statistical Reasoning | Strong |
| Data Science & ML | Strong |
| AI & LLM Literacy | Good |
| Communication & Storytelling | Strong after documentation |
| Creativity & Initiative | Strong through end-to-end platform and AI assistant concept |
| Professionalism | Strong through modular code and reproducibility |

---

## 22. Final Conclusion

This project demonstrates a complete end-to-end data workflow using real-world Airbnb market data.

It begins with raw data ingestion and profiling, then continues through cleaning, validation, transformation, warehouse design, SQL analytics, EDA, statistical testing, machine learning, explainability, and responsible AI documentation.

The final solution is more than a notebook analysis. It is a reproducible market intelligence platform with reusable source code, documented assumptions, analytical outputs, ML results, and a clear path for future AI-powered extension.