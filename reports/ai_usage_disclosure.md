# AI Usage Disclosure

## Project

Inside Airbnb Market Intelligence Platform — Data Engineering, Analytics & AI

## Purpose

This document explains how AI tools were used during the project.

AI tools were used as a support resource for planning, debugging, explanation, documentation, and interpretation. AI was not used to fabricate results or replace human understanding of the dataset.

## How AI Was Used

AI assistance was used for:

- Breaking the project into clear phases
- Explaining data engineering and machine learning concepts
- Debugging Python, pandas, DuckDB, and scikit-learn issues
- Improving code structure and repository organization
- Planning reusable pipeline scripts
- Reviewing statistical and machine learning interpretations
- Drafting documentation such as README, model card, architecture notes, and final report
- Improving business-friendly wording for insights and limitations

## Human Verification

All important AI-generated suggestions were checked against actual project outputs.

Verification was done using:

- Dataset schema outputs
- Notebook results
- Terminal outputs
- Data quality reports
- Row count checks
- DuckDB warehouse validation
- Statistical test outputs
- Machine learning evaluation metrics
- Feature importance results
- Residual analysis outputs

## Responsible AI Practices

The project followed responsible AI practices:

- Dataset assumptions were verified before use.
- AI suggestions were not accepted blindly.
- Target leakage risks were reviewed and controlled.
- Limitations were documented clearly.
- Proxy metrics were explained carefully.
- Model outputs were interpreted as decision-support, not final truth.

## Important Example

The calendar dataset was checked before revenue analysis. It was confirmed that the Amsterdam calendar file does not contain daily price or adjusted price columns.

Because of this, calendar data was used for availability and occupancy proxy analysis only. It was not used for actual daily revenue analysis.

## AI Usage Boundary

AI was not used to create fake data, fake results, or unsupported conclusions.

The final conclusions are based on executed code, generated outputs, and human interpretation.

## Final Statement

AI tools supported the development process, but the project owner remained responsible for validating, understanding, and presenting the final work.