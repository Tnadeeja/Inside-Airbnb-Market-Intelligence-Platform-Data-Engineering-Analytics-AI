# Engineering Decision Log

## Decision 001: Base Listing Table Selection

**Decision:** Use `summary_listings` as the base listing universe and enrich it with fields from `detailed_listings`.

**Reasoning:**  
The summary listings table contains 10,465 unique listings, while detailed listings contains 10,369. Calendar data also contains 10,465 unique listing IDs, which aligns with the summary listings table.

**Trade-off:**  
Some listings will not have detailed metadata such as amenities, descriptions, or host profile fields.

**Impact:**  
This approach preserves market coverage while still allowing rich analysis for listings with detailed metadata.

---

## Decision 002: Calendar Dataset Usage

**Decision:** Use the calendar dataset for availability and stay-policy analysis, not direct pricing analysis.

**Reasoning:**  
The Amsterdam calendar snapshot contains `listing_id`, `date`, `available`, `minimum_nights`, and `maximum_nights`. It does not contain `price` or `adjusted_price` fields.

**Trade-off:**  
Daily price trends, weekend price premium, and direct calendar-based revenue cannot be calculated from the calendar file.

**Impact:**  
Calendar-derived features will focus on availability rate, occupancy proxy, weekend/weekday availability, and stay-policy metrics.

## Decision 003: Unknown Host Dimension Record

**Decision:** Add an Unknown Host record to `dim_host` using `host_key = -1`.

**Reasoning:**  
During star schema validation, 96 fact rows had missing host_id values and therefore could not join to a known host dimension record.

**Trade-off:**  
The original host identity for these 96 listings remains unknown. However, assigning them to an Unknown Host record preserves all listing records and maintains warehouse referential consistency.

**Impact:**  
The fact table has no missing host keys, and records with incomplete host metadata remain visible for analysis instead of being dropped.


---

# 3. Improve `reports/decision_log.md`

Your current decision log is good. Keep your existing content and add these decisions under Decision 003:

```markdown
---

## Decision 004: Use DuckDB as Local Analytical Warehouse

**Decision:** Use DuckDB as the analytical warehouse for this project.

**Reasoning:**  
DuckDB is lightweight, fast for analytical queries, works well with parquet files, and is suitable for local data engineering workflows.

**Trade-off:**  
DuckDB is not a full enterprise cloud warehouse like Snowflake, BigQuery, or Redshift.

**Impact:**  
The project can build a reproducible local warehouse without external infrastructure.

---

## Decision 005: Build Reusable Source Code Under `src/`

**Decision:** Convert important notebook logic into reusable Python modules under `src/`.

**Reasoning:**  
Notebook-only projects are harder to reproduce and review. Reusable scripts improve code quality, project structure, and production readiness.

**Trade-off:**  
This adds extra development time and some repeated logic from notebooks.

**Impact:**  
The project now supports reusable ingestion, profiling, validation, cleaning, transformation, warehouse, and ML workflows.

---

## Decision 006: Keep Raw Data, Processed Data, Warehouse, and Model Artifacts Out of Git

**Decision:** Do not commit large generated files such as raw datasets, processed parquet files, DuckDB database files, and model artifacts.

**Reasoning:**  
These files can be large and can be recreated by running the pipeline.

**Trade-off:**  
A reviewer needs to download the raw data and run the pipeline to recreate generated artifacts.

**Impact:**  
The repository stays clean, lightweight, and professional.

---

## Decision 007: Use Random Forest as Final Price Prediction Model

**Decision:** Select the Random Forest Regressor as the final machine learning model.

**Reasoning:**  
It achieved the best overall performance among tested models, with the lowest RMSE and highest R² score.

**Trade-off:**  
Random Forest is less directly interpretable than simple linear regression.

**Impact:**  
The final model provides stronger predictive performance while still allowing feature importance analysis.

---

## Decision 008: Document AI Usage and Open Innovation Separately

**Decision:** Create separate documentation for AI usage and open innovation.

**Reasoning:**  
The assignment evaluates AI and LLM literacy. Clear documentation helps show responsible AI use and future AI potential.

**Trade-off:**  
The AI assistant is documented as a future concept rather than a fully built application.

**Impact:**  
The project honestly demonstrates AI literacy, responsible AI awareness, and creativity without overstating implementation.