# AI / LLM Usage and Open Innovation

## Project

Inside Airbnb Market Intelligence Platform — Data Engineering, Analytics & AI

## Purpose of This Document

This document explains how AI and LLM tools were used responsibly during the project and proposes an open innovation extension for the platform.

The goal is to demonstrate AI literacy, responsible use of AI tools, creativity, and awareness of AI limitations.

---

## 1. AI / LLM Usage in This Project

AI tools were used as a learning, planning, debugging, and documentation support tool during the development of this project.

AI assistance was used to support:

- Project planning and phase breakdown
- Data engineering workflow design
- Python debugging support
- Explanation of data cleaning and transformation logic
- Statistical analysis interpretation
- Machine learning workflow planning
- Feature importance and residual analysis explanation
- Repository structure improvement
- Documentation drafting and review
- Final report and README planning

AI was not used as a replacement for understanding the data. Outputs were reviewed, tested, and validated against actual project results.

---

## 2. Human Verification Process

The project followed a human-in-the-loop approach.

AI suggestions were checked using:

- Actual dataset schema outputs
- Notebook execution results
- Terminal outputs
- Data quality reports
- Row count validations
- Model evaluation metrics
- Feature importance outputs
- Residual analysis outputs
- Manual interpretation and correction

For example, the calendar dataset was checked before analysis. It was confirmed that the Amsterdam calendar file did not contain daily price or adjusted price columns. Therefore, calendar data was used only for availability and occupancy proxy analysis, not actual daily revenue analysis.

---

## 3. Responsible AI Practices

The project followed responsible AI practices in the following ways:

### 3.1 Schema-first development

AI-generated assumptions were not accepted blindly.

Dataset columns and shapes were verified before building logic.

### 3.2 Assumption logging

Important project assumptions were documented, including:

- Occupancy proxy is based on unavailable days.
- Unavailable days may include booked days or host-blocked days.
- Estimated revenue proxy is not actual revenue.
- Missing price values reduce ML coverage.
- Calendar data does not include daily price fields.

### 3.3 Target leakage control

The machine learning workflow explicitly excluded target leakage fields.

The field `estimated_revenue_proxy` was excluded because it is calculated using:

```text
price_numeric × unavailable_days
```

Using this field to predict price would leak the target into the model.

### 3.4 Model limitation documentation

The model card documents the model purpose, limitations, intended use, and not-intended use.

### 3.5 Human interpretation

AI and ML outputs were translated into cautious business language.

The project avoids unsupported claims such as:

```
Bedrooms cause higher price.
```

Instead, it uses careful wording such as:

```
Bedrooms are one of the strongest predictive signals used by the model.
```

---

## 4. AI Usage Boundaries

AI assistance was not used to fabricate results.

The project does not claim that AI tools independently performed the analysis.

The final results are based on:

- Executed Python notebooks
- Reusable Python scripts
- Generated CSV reports
- Statistical test outputs
- Machine learning evaluation outputs
- SQL warehouse tables
- Visual analysis outputs

AI was used as a support tool, while the project owner remained responsible for validating and understanding the work.

---

## 5. Data Privacy and Safety

This project uses publicly available Inside Airbnb data.

No private customer records, confidential company data, or sensitive personal datasets were intentionally used in the analysis.

The repository also avoids committing large generated artifacts such as raw datasets, processed parquet files, local warehouse files, and model artifacts.

---

## 6. Open Innovation Concept

## AI-Powered Airbnb Market Intelligence Assistant

A future extension of this project is an AI-powered market intelligence assistant that helps business users explore Airbnb market insights using natural language.

The assistant would sit on top of the DuckDB warehouse, analytical outputs, and model results.

---

## 7. Proposed User Capabilities

The AI assistant could answer questions such as:

- Which neighbourhoods have the highest estimated revenue proxy?
- Which room types perform best in Amsterdam?
- Why is a listing predicted to have a higher price?
- Which features influence Airbnb price the most?
- Where does the model make large prediction errors?
- Which neighbourhoods have high supply but lower median price?
- Which host portfolio segments show stronger market activity?
- What are the risks of interpreting occupancy proxy as real occupancy?

---

## 8. Proposed System Architecture

```
User Question
     |
     v
LLM Interface
     |
     v
Query Planner / Guardrails
     |
     v
DuckDB Warehouse + Analytics Outputs + ML Reports
     |
     v
Validated Answer with Charts / Tables / Caveats
```

The assistant should not directly guess answers. It should retrieve information from project outputs and provide grounded explanations.

---

## 9. Possible Features

### 9.1 Natural Language Analytics

Users could ask business questions in plain English.

Example:

```
Which neighbourhoods look attractive for entire home listings?
```

The assistant could translate the question into a SQL query and summarize the result.

### 9.2 Price Prediction Explanation

The assistant could explain price prediction results using model feature importance and listing attributes.

Example:

```
This listing is predicted to be higher priced because it has more bedrooms, stronger review value, and is located in a higher-price neighbourhood.
```

### 9.3 Host Strategy Recommendations

The assistant could generate business-friendly recommendations.

Example:

```
Private room listings have lower average price and occupancy proxy compared with entire homes. Hosts may need to focus on review quality, amenities, and competitive pricing.
```

### 9.4 Risk-Aware Insights

The assistant could include automatic caveats.

Example:

```
This revenue value is an estimated proxy, not actual confirmed revenue.
```

### 9.5 Report Generation

The assistant could generate a weekly or monthly market intelligence summary.

Possible sections:

- Market overview
- Top neighbourhoods
- Room type performance
- Review trends
- Pricing drivers
- Model limitations

---

## 10. Guardrails for the AI Assistant

The assistant should include the following guardrails:

- Do not treat estimated revenue proxy as actual revenue.
- Do not treat occupancy proxy as confirmed occupancy.
- Do not make claims about individual hosts or guests beyond the dataset.
- Do not make legal, financial, or regulatory recommendations.
- Always mention limitations when using proxy metrics.
- Use SQL/database outputs where possible instead of guessing.
- Provide source table or report reference for important answers.
- Avoid overconfident explanations for unusual luxury listings.

---

## 11. Why This Extension Adds Value

The proposed AI assistant adds value because it makes the market intelligence platform easier for non-technical users.

Instead of manually reading notebooks, SQL outputs, and CSV reports, a business user could ask questions naturally and receive:

- Clear explanations
- Relevant KPIs
- Supporting evidence
- Business interpretation
- Limitations and assumptions

This improves communication, accessibility, and decision support.

---

## 12. Future Implementation Plan

A future version could be implemented using:

- DuckDB as the analytical backend
- Streamlit as a simple user interface
- A retrieval layer over generated reports
- SQL query templates
- LLM-based explanation generation
- Guardrails for proxy metrics and model limitations

Possible implementation stages:

1. Build a Streamlit dashboard
2. Add predefined business questions
3. Add natural language question input
4. Connect questions to SQL query templates
5. Add LLM-generated explanations
6. Add model explanation summaries
7. Add safety and limitation messages

---

## 13. Final AI / LLM Literacy Conclusion

This project demonstrates responsible AI literacy in two ways.

First, AI tools were used carefully as development and learning support, with human verification and documented assumptions.

Second, the project proposes a realistic AI-powered market intelligence assistant as a future extension, while clearly documenting required guardrails and limitations.

This approach shows both practical AI usage and responsible awareness of AI risks.
