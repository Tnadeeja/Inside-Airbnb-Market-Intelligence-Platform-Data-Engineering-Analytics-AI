# DDL - Warehouse Schema

This folder documents the DuckDB warehouse schema used in the Inside Airbnb Market Intelligence Platform.

## Files

### `01_create_star_schema.sql`

Defines the intended star schema structure:

- `dim_listing`
- `dim_host`
- `dim_neighbourhood`
- `fact_listing_market`

### `02_create_analytics_tables.sql`

Defines the reusable analytical summary table structures:

- `market_overview`
- `room_type_summary`
- `neighbourhood_summary`
- `host_portfolio_summary`
- `review_score_summary`

## Notes

The actual DuckDB warehouse is built using:

```bash
python -m src.warehouse.duckdb_builder