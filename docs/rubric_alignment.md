# Rubric Alignment

## Project

Inside Airbnb Market Intelligence Platform — Data Engineering, Analytics & AI

## Purpose

This document maps the project work to the assignment evaluation criteria.

The project was designed to demonstrate data engineering, analytical thinking, statistical reasoning, machine learning, AI literacy, communication, creativity, and professional project structure.

---

## 1. Data Engineering Fundamentals

### What the assignment evaluates

- Data ingestion
- Data profiling
- Data cleaning
- Data modeling
- Pipeline design

### How this project addresses it

This project implements an end-to-end data engineering workflow using Inside Airbnb data for Amsterdam.

Completed work includes:

- Raw data file validation
- Dataset inventory generation
- Schema profiling
- Missing value profiling
- Data quality validation
- Summary listings cleaning
- Calendar cleaning and aggregation
- Reviews cleaning and aggregation
- Final listing master table creation
- DuckDB warehouse creation
- Star schema design
- Reusable pipeline scripts under `src/`

### Evidence in repository

```text
src/ingestion/raw_data_loader.py
src/profiling/dataset_profiler.py
src/validation/data_quality_checks.py
src/cleaning/listings_cleaner.py
src/cleaning/calendar_cleaner.py
src/cleaning/reviews_cleaner.py
src/transformation/listing_master_builder.py
src/warehouse/duckdb_builder.py
src/pipeline_runner.py
```

Supporting outputs:

```
reports/data_quality/
reports/analytics_outputs/
data/README.md
docs/architecture.md
docs/warehouse_design.md
sql/ddl/
```

### Key strength

The project goes beyond notebook exploration by implementing a reusable Python pipeline and a local analytical warehouse.

---

## 2. Analytical Thinking

### What the assignment evaluates

- Exploratory data analysis
- Statistical reasoning
- Business interpretation
- Ability to find useful patterns

### How this project addresses it

The project performs business-focused analysis on the Amsterdam Airbnb market.

Main analysis areas include:

- Market overview
- Room type performance
- Neighbourhood performance
- Host portfolio behavior
- Availability and occupancy proxy
- Review score patterns
- Price distribution and outliers
- Correlation analysis

### Evidence in repository

```
notebooks/03_eda_business_analysis.ipynb
reports/analytics_outputs/
reports/figures/
sql/analysis_queries/
```

### Example insights

- Entire homes/apartments dominate Amsterdam Airbnb supply.
- De Baarsjes - Oud-West is one of the largest and highest revenue proxy neighbourhoods.
- Price is right-skewed, so median price is often more reliable than average price.
- Availability and occupancy proxy vary across room types and neighbourhoods.
- Review scores are highly concentrated near the upper range, suggesting review score inflation.

### Key strength

The analysis connects technical results to business meaning instead of only producing charts.

---

## 3. Statistical Reasoning

### What the assignment evaluates

- Correct use of statistical methods
- Ability to validate patterns
- Interpretation of significance and effect size

### How this project addresses it

The project uses non-parametric statistical tests because Airbnb price and review score distributions are skewed and contain outliers.

Statistical analysis includes:

- Kruskal-Wallis tests
- Mann-Whitney U pairwise comparisons
- Bonferroni correction
- Effect size interpretation
- Spearman correlation analysis

### Evidence in repository

```
notebooks/04_statistical_analysis.ipynb
reports/statistical_analysis/
```

### Statistical questions tested

- Do prices differ significantly by room type?
- Do prices differ by host portfolio segment?
- Does occupancy proxy differ by room type?
- Do review scores differ by room type?
- Which numeric features are significantly associated with price?

### Key strength

The project does not rely only on visual analysis. It validates major patterns using statistical testing and effect sizes.

---

## 4. Data Science & Machine Learning

### What the assignment evaluates

- Feature engineering
- Model building
- Model validation
- Explainability

### How this project addresses it

The project builds a supervised regression model to predict Airbnb listing prices.

Completed ML work includes:

- ML dataset preparation
- Feature selection
- Target leakage prevention
- Numeric and categorical preprocessing
- Train/test split
- Baseline model comparison
- Multiple regression model comparison
- Random Forest final model selection
- Feature importance analysis
- Residual and prediction error analysis
- Model card documentation

### Evidence in repository

```
notebooks/05_ml_price_prediction.ipynb
src/ml/train_price_model.py
docs/model_card.md
reports/machine_learning/
reports/figures/machine_learning/
```

### Models compared

- Dummy Median Baseline
- Linear Regression
- Ridge Regression
- Random Forest Regressor
- Gradient Boosting Regressor

### Final model

```
Random Forest Regressor
```

### Final performance

MetricValueMAE88.40RMSE147.30R² Score0.5009

### Baseline comparison

MetricValueBaseline RMSE213.50RMSE Improvement66.20RMSE Improvement Percentage31.01%

### Key strength

The ML work includes model explainability, baseline comparison, error analysis, and documented limitations.

---

## 5. AI & LLM Literacy

### What the assignment evaluates

- Responsible AI tool usage
- Effective use of AI support
- Awareness of AI limitations
- Creative use of AI or LLM concepts

### How this project addresses it

AI tools were used as learning and development support, not as a replacement for understanding.

AI assistance was used for:

- Structuring project phases
- Debugging Python errors
- Explaining data engineering concepts
- Improving documentation
- Reviewing analysis interpretation
- Planning reusable pipeline code
- Supporting README and report writing

The project also documents responsible AI usage and limitations.

### Evidence in repository

```
reports/ai_usage_disclosure.md
docs/model_card.md
docs/rubric_alignment.md
```

### Responsible AI practices

- AI-generated suggestions were reviewed before use.
- Dataset schema was verified from actual outputs.
- Assumptions and limitations were documented.
- Model predictions were not treated as final decisions.
- Target leakage was identified and controlled.
- Business interpretations were written with caution.

### Key strength

The project demonstrates AI-assisted development while maintaining human verification, reproducibility, and responsible interpretation.

---

## 6. Communication & Storytelling

### What the assignment evaluates

- Ability to explain technical findings in business language
- Clear documentation
- Insight communication
- Final presentation quality

### How this project addresses it

The project translates data engineering, analytics, statistics, and ML work into business-focused explanations.

Communication outputs include:

- Architecture documentation
- Warehouse design documentation
- Model card
- Rubric alignment
- Data directory documentation
- Warehouse README
- Models README
- SQL README
- Analysis notebooks with interpretations
- Final report planned

### Evidence in repository

```
docs/architecture.md
docs/warehouse_design.md
docs/model_card.md
docs/rubric_alignment.md
notebooks/
reports/figures/
README.md
```

### Key storytelling themes

- Which Airbnb segments dominate the market?
- Which neighbourhoods show stronger market activity?
- How do room type and host type affect price?
- What factors help predict price?
- Where does the ML model struggle?
- What are the limitations of proxy metrics?

### Key strength

The project explains not only what was done, but why it matters for business decision-making.

---

## 7. Creativity & Initiative

### What the assignment evaluates

- Going beyond the basic prompt
- Building something novel
- Showing independent thinking

### How this project addresses it

The project goes beyond basic EDA by building a full market intelligence platform.

Extra work includes:

- Reusable Python pipeline under `src/`
- DuckDB analytical warehouse
- Star schema design
- Statistical testing
- Machine learning model
- Model explainability
- Residual analysis
- Responsible AI documentation
- Professional project structure
- Planned AI-powered market intelligence assistant concept

### Evidence in repository

```
src/
sql/ddl/
docs/
reports/
models/
warehouse/
```

### Open innovation direction

A future extension is an AI-powered Airbnb Market Intelligence Assistant that could help users ask natural language questions such as:

- Which neighbourhoods have high revenue potential?
- Why is a listing predicted to be expensive?
- Which features should a host improve?
- Which room types perform best in each neighbourhood?
- What are the risks in interpreting occupancy proxy?

### Key strength

The project is designed as a portfolio-level end-to-end platform rather than a single notebook analysis.

---

## 8. Professionalism

### What the assignment evaluates

- Code quality
- Documentation
- Reproducibility
- Folder structure
- Clean submission

### How this project addresses it

The repository is organized into a professional data project structure.

Professional practices include:

- Modular Python source code
- Reusable pipeline runner
- Clear folder structure
- `.gitignore` for generated and large files
- README files for data, models, warehouse, SQL, and source code
- Generated outputs separated from source code
- DDL documentation
- Model card
- Architecture documentation
- Reproducibility instructions

### Evidence in repository

```
src/
docs/
sql/
reports/
data/README.md
warehouse/README.md
models/README.md
.gitignore
requirements.txt
```

### Reproducibility commands

Full data pipeline:

```
python -m src.pipeline_runner
```

ML training:

```
python -m src.ml.train_price_model
```

### Key strength

The project can be reviewed, rerun, and understood by another person without depending only on notebooks.

---

## Overall Rubric Summary

CompetencyProject CoverageData Engineering FundamentalsStrongAnalytical ThinkingStrongStatistical ReasoningStrongData Science & MLStrongAI & LLM LiteracyGood, with final AI section plannedCommunication & StorytellingGood, final report still neededCreativity & InitiativeGood, open innovation section plannedProfessionalismStrong after repository cleanup and documentation

---

## Remaining Improvements Before Final Submission

The main remaining tasks are:

1. Finalize the main `README.md`
2. Create final project report
3. Add AI/LLM usage and open innovation documentation
4. Add dashboard or visual storytelling summary
5. Review all generated outputs
6. Run final reproducibility check
7. Prepare final submission package

---

## Final Assessment Position

This project demonstrates a strong end-to-end data workflow.

It covers raw data ingestion, profiling, validation, cleaning, feature engineering, warehouse design, SQL analytics, EDA, statistical testing, machine learning, explainability, and professional documentation.

The remaining focus is final communication, storytelling, and submission polish.
