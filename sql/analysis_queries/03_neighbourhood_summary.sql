-- Neighbourhood Summary
-- Purpose: Compares supply, pricing, availability, occupancy proxy, review activity, and revenue proxy by neighbourhood.

SELECT
    dn.neighbourhood,

    COUNT(*) AS listing_count,
    COUNT(DISTINCT f.host_id) AS known_host_count,

    ROUND(AVG(f.price_numeric), 2) AS avg_price,
    ROUND(MEDIAN(f.price_numeric), 2) AS median_price,

    ROUND(AVG(f.availability_rate), 4) AS avg_availability_rate,
    ROUND(AVG(f.occupancy_proxy), 4) AS avg_occupancy_proxy,

    ROUND(AVG(f.review_scores_rating), 2) AS avg_review_score,
    SUM(f.detailed_review_count) AS total_reviews,
    ROUND(AVG(f.detailed_review_count), 2) AS avg_reviews_per_listing,

    ROUND(SUM(f.estimated_revenue_proxy), 2) AS total_revenue_proxy,
    ROUND(AVG(f.estimated_revenue_proxy), 2) AS avg_revenue_proxy,

    SUM(CASE WHEN f.price_numeric IS NULL THEN 1 ELSE 0 END) AS listings_missing_price
FROM fact_listing_market f
LEFT JOIN dim_neighbourhood dn
    ON f.neighbourhood_key = dn.neighbourhood_key
GROUP BY
    dn.neighbourhood
ORDER BY
    total_revenue_proxy DESC;