# Inside Airbnb Market Intelligence Platform — Project Tracker

## Project Goal

Build a professional data engineering, analytics, and AI portfolio project using the Inside Airbnb Amsterdam dataset.

The project focuses on:
- dataset familiarization
- data quality profiling
- data cleaning
- relationship mapping
- listing master table creation
- EDA
- statistical analysis
- machine learning
- NLP/AI experiments
- final reporting and business recommendations

---

## Current Scope

### City
Amsterdam, North Holland, The Netherlands

### Snapshot Date
15 June 2026

### Current Strategy
Use Amsterdam as the fully implemented market first.  
Design the pipeline so it can be extended to London and Paris later.

---

## Confirmed Raw Dataset Inventory

| Dataset | File | Rows | Columns | Confirmed Purpose |
|---|---|---:|---:|---|
| detailed_listings | listings.csv.gz | 10,369 | 90 | Rich listing, host, property, review score, and amenity metadata |
| calendar | calendar.csv.gz | 3,819,725 | 5 | Daily availability and stay policy records |
| detailed_reviews | reviews.csv.gz | 545,162 | 6 | Review-level data with comments for NLP |
| summary_listings | listings.csv | 10,465 | 19 | Base listing universe for analysis and visualisation |
| summary_reviews | reviews.csv | 545,162 | 2 | Review dates linked to listing IDs |
| neighbourhoods | neighbourhoods.csv | 22 | 2 | Neighbourhood lookup |
| neighbourhoods_geojson | neighbourhoods.geojson | Not loaded yet | Not loaded yet | Geospatial boundaries |

---

## Confirmed Calendar Schema

The calendar file contains:
- listing_id
- date
- available
- minimum_nights
- maximum_nights

The calendar file does not contain:
- price
- adjusted_price

### Calendar Limitation

Calendar-based daily pricing, weekend price premium, and direct revenue estimation cannot be calculated from this calendar snapshot.  
Calendar-derived metrics will focus on availability, occupancy proxy, weekend/weekday availability, and stay-policy metrics.

---

## Completed Work

### Phase 0 — Project Setup
- Project folder created
- Python virtual environment created
- Raw data downloaded
- Notebook started
- Reports folder created

### Phase 1 — Dataset Familiarization
- Dataset inventory created
- Schema profile created
- Missing value analysis created
- Duplicate summary created
- Key quality summary created
- Domain validation summary created
- Relationship mapping created
- Listing ID coverage analysis created

### Phase 2 — Data Engineering Cleaning
- Cleaned base listing table created from summary listings
- Detailed listings enrichment created
- Calendar data cleaned
- Calendar listing-level metrics created

---

## Key Engineering Decisions

### Decision 001 — Base Listing Table
Use summary_listings as the base listing universe because it has 10,465 listings and aligns with calendar coverage.  
Use detailed_listings as an enrichment source because it has richer metadata but fewer listing records.

### Decision 002 — Calendar Dataset Usage
Use calendar data for availability and stay-policy analysis only.  
Do not use it for direct daily pricing because price columns are not available in this snapshot.

---

## Current Stage

Currently working on:

Phase 2 — Data Engineering

Next immediate task:

Join calendar_listing_metrics into listing_master_base to create a stronger listing_master table.

---

## Not Started Yet

- Review data cleaning and aggregation
- Neighbourhood enrichment
- Final listing master table
- DuckDB warehouse
- Star schema
- SQL analysis queries
- EDA
- Statistical testing
- ML price prediction
- NLP/AI experiments
- Dashboard
- Final report
- README finalization
- AI usage disclosure

## Phase 7 - Repository Hardening and Reusable Pipeline Code

Started converting notebook-based logic into reusable Python modules under `src/`.

Completed:
- Added project-wide configuration in `src/config.py`
- Added Python package initialization files
- Added `src/README.md`
- Created reusable path constants for data, reports, warehouse, SQL, and model artifacts