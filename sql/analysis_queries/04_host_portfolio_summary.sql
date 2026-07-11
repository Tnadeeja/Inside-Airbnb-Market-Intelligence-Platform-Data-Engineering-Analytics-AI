-- Host Portfolio Summary
-- Purpose: Compares listing behavior across host portfolio segments.

SELECT
    dh.host_portfolio_segment,

    COUNT(*) AS listing_count,
    COUNT(DISTINCT f.host_id) AS known_host_count,

    ROUND(AVG(f.price_numeric), 2) AS avg_price,
    ROUND(MEDIAN(f.price_numeric), 2) AS median_price,

    ROUND(AVG(f.availability_rate), 4) AS avg_availability_rate,
    ROUND(AVG(f.occupancy_proxy), 4) AS avg_occupancy_proxy,

    ROUND(AVG(f.review_scores_rating), 2) AS avg_review_score,
    SUM(f.detailed_review_count) AS total_reviews,

    ROUND(SUM(f.estimated_revenue_proxy), 2) AS total_revenue_proxy,
    ROUND(AVG(f.estimated_revenue_proxy), 2) AS avg_revenue_proxy
FROM fact_listing_market f
LEFT JOIN dim_host dh
    ON f.host_key = dh.host_key
GROUP BY
    dh.host_portfolio_segment
ORDER BY
    listing_count DESC;