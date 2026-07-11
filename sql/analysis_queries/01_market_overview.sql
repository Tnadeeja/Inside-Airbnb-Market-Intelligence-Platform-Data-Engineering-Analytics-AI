-- Market Overview
-- Purpose: Provides a one-row executive summary of the Amsterdam Airbnb market.

SELECT
    COUNT(*) AS total_listings,
    COUNT(DISTINCT host_id) AS total_known_hosts,
    COUNT(DISTINCT neighbourhood) AS total_neighbourhoods,

    ROUND(AVG(price_numeric), 2) AS avg_listing_price,
    ROUND(MEDIAN(price_numeric), 2) AS median_listing_price,

    ROUND(AVG(availability_rate), 4) AS avg_availability_rate,
    ROUND(AVG(occupancy_proxy), 4) AS avg_occupancy_proxy,

    SUM(CASE WHEN has_reviews = TRUE THEN 1 ELSE 0 END) AS listings_with_reviews,
    SUM(CASE WHEN has_reviews = FALSE THEN 1 ELSE 0 END) AS listings_without_reviews,

    SUM(detailed_review_count) AS total_detailed_reviews,
    ROUND(AVG(review_scores_rating), 2) AS avg_review_score,

    ROUND(SUM(estimated_revenue_proxy), 2) AS total_revenue_proxy,
    ROUND(AVG(estimated_revenue_proxy), 2) AS avg_revenue_proxy,

    SUM(CASE WHEN price_numeric IS NULL THEN 1 ELSE 0 END) AS listings_missing_price
FROM fact_listing_market;