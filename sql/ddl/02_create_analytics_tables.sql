-- ============================================================
-- Inside Airbnb Market Intelligence Platform
-- Analytical Summary Tables DDL
--
-- Purpose:
-- Documents the reusable analytical summary tables created
-- in the DuckDB warehouse.
-- ============================================================


CREATE TABLE IF NOT EXISTS market_overview (
    total_listings BIGINT,
    total_known_hosts BIGINT,
    total_neighbourhoods BIGINT,
    avg_listing_price DOUBLE,
    median_listing_price DOUBLE,
    avg_availability_rate DOUBLE,
    avg_occupancy_proxy DOUBLE,
    listings_with_reviews BIGINT,
    listings_without_reviews BIGINT,
    total_detailed_reviews BIGINT,
    avg_review_score DOUBLE,
    total_estimated_revenue_proxy DOUBLE,
    listings_missing_or_invalid_price BIGINT
);


CREATE TABLE IF NOT EXISTS room_type_summary (
    room_type VARCHAR,
    listing_count BIGINT,
    avg_price DOUBLE,
    median_price DOUBLE,
    avg_availability_rate DOUBLE,
    avg_occupancy_proxy DOUBLE,
    total_detailed_reviews BIGINT,
    total_estimated_revenue_proxy DOUBLE
);


CREATE TABLE IF NOT EXISTS neighbourhood_summary (
    neighbourhood VARCHAR,
    listing_count BIGINT,
    avg_price DOUBLE,
    median_price DOUBLE,
    avg_availability_rate DOUBLE,
    avg_occupancy_proxy DOUBLE,
    total_detailed_reviews BIGINT,
    total_estimated_revenue_proxy DOUBLE
);


CREATE TABLE IF NOT EXISTS host_portfolio_summary (
    host_portfolio_segment VARCHAR,
    listing_count BIGINT,
    host_count BIGINT,
    avg_price DOUBLE,
    median_price DOUBLE,
    avg_availability_rate DOUBLE,
    avg_occupancy_proxy DOUBLE,
    total_estimated_revenue_proxy DOUBLE
);


CREATE TABLE IF NOT EXISTS review_score_summary (
    review_score_band VARCHAR,
    listing_count BIGINT,
    avg_price DOUBLE,
    median_price DOUBLE,
    avg_availability_rate DOUBLE,
    avg_occupancy_proxy DOUBLE,
    total_detailed_reviews BIGINT,
    total_estimated_revenue_proxy DOUBLE
);