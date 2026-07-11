# SQL Analysis Queries

This folder contains standalone SQL queries used for business analysis against the DuckDB star schema.

## Query Files

1. `01_market_overview.sql`  
   Executive-level market summary.

2. `02_room_type_summary.sql`  
   Room type comparison by supply, price, availability, review activity, and revenue proxy.

3. `03_neighbourhood_summary.sql`  
   Neighbourhood-level market comparison.

4. `04_host_portfolio_summary.sql`  
   Host portfolio segment comparison.

5. `05_review_score_summary.sql`  
   Review score band analysis.

6. `06_top_neighbourhood_room_type_revenue.sql`  
   Top neighbourhood and room type combinations by estimated revenue proxy.

## Important Note

`estimated_revenue_proxy` is not actual Airbnb revenue.  
It is a proxy calculated using listing-level price and unavailable calendar days.  
Unavailable days may include both booked nights and host-blocked dates.