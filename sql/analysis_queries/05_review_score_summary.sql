-- Review Score Summary
-- Purpose: Groups listings by review score band and compares pricing, availability, occupancy proxy, and review activity.

SELECT
    CASE
        WHEN review_scores_rating IS NULL THEN 'No rating'
        WHEN review_scores_rating >= 4.8 THEN 'Excellent'
        WHEN review_scores_rating >= 4.5 THEN 'Very good'
        WHEN review_scores_rating >= 4.0 THEN 'Good'
        ELSE 'Below 4.0'
    END AS review_score_band,

    COUNT(*) AS listing_count,

    ROUND(AVG(price_numeric), 2) AS avg_price,
    ROUND(MEDIAN(price_numeric), 2) AS median_price,

    ROUND(AVG(availability_rate), 4) AS avg_availability_rate,
    ROUND(AVG(occupancy_proxy), 4) AS avg_occupancy_proxy,

    SUM(detailed_review_count) AS total_reviews,
    ROUND(AVG(detailed_review_count), 2) AS avg_reviews_per_listing,

    ROUND(SUM(estimated_revenue_proxy), 2) AS total_revenue_proxy,
    ROUND(AVG(estimated_revenue_proxy), 2) AS avg_revenue_proxy
FROM fact_listing_market
GROUP BY
    review_score_band
ORDER BY
    listing_count DESC;