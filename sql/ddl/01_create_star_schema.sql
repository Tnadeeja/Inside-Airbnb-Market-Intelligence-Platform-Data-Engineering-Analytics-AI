-- ============================================================
-- Inside Airbnb Market Intelligence Platform
-- Star Schema DDL
--
-- Purpose:
-- Defines the analytical warehouse star schema used for
-- listing, host, neighbourhood, and market performance analysis.
--
-- Note:
-- The production build script creates these tables using
-- CREATE OR REPLACE TABLE AS SELECT from the final listing master.
-- This DDL file documents the intended schema structure.
-- ============================================================


CREATE TABLE IF NOT EXISTS dim_listing (
    listing_key BIGINT,
    listing_id BIGINT,
    listing_name VARCHAR,
    room_type VARCHAR,
    property_type VARCHAR,
    minimum_nights DOUBLE,
    accommodates DOUBLE,
    bathrooms DOUBLE,
    bedrooms DOUBLE,
    beds DOUBLE,
    amenities_count BIGINT,
    has_valid_price BOOLEAN,
    has_valid_coordinates BOOLEAN,
    license VARCHAR
);


CREATE TABLE IF NOT EXISTS dim_host (
    host_key BIGINT,
    host_id BIGINT,
    host_name VARCHAR,
    host_since TIMESTAMP,
    host_is_superhost VARCHAR,
    host_identity_verified VARCHAR,
    calculated_host_listings_count DOUBLE,
    host_portfolio_segment VARCHAR
);


CREATE TABLE IF NOT EXISTS dim_neighbourhood (
    neighbourhood_key BIGINT,
    neighbourhood VARCHAR,
    neighbourhood_group VARCHAR,
    neighbourhood_listing_count BIGINT,
    neighbourhood_avg_price DOUBLE,
    neighbourhood_median_price DOUBLE,
    neighbourhood_avg_availability_rate DOUBLE,
    neighbourhood_avg_occupancy_proxy DOUBLE,
    neighbourhood_total_reviews DOUBLE
);


CREATE TABLE IF NOT EXISTS fact_listing_market (
    fact_key BIGINT,
    listing_key BIGINT,
    host_key BIGINT,
    neighbourhood_key BIGINT,
    listing_id BIGINT,

    price_numeric DOUBLE,
    has_valid_price BOOLEAN,

    calendar_days BIGINT,
    available_days BIGINT,
    unavailable_days BIGINT,
    availability_rate DOUBLE,
    occupancy_proxy DOUBLE,
    weekend_availability_rate DOUBLE,
    weekday_availability_rate DOUBLE,

    number_of_reviews DOUBLE,
    reviews_per_month DOUBLE,
    detailed_review_count BIGINT,
    unique_reviewer_count BIGINT,
    detailed_reviews_last_365d BIGINT,
    avg_reviews_per_year DOUBLE,
    comment_coverage_rate DOUBLE,

    review_scores_rating DOUBLE,
    review_scores_cleanliness DOUBLE,
    review_scores_location DOUBLE,
    review_scores_value DOUBLE,

    estimated_revenue_proxy DOUBLE
);