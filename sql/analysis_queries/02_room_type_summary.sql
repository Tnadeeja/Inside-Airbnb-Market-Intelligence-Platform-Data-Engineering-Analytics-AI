-- Room Type Summary
-- Purpose: Compares market supply, pricing, availability, occupancy proxy, reviews, and revenue proxy by room type.

SELECT
    dl.room_type,

    COUNT(*) AS listing_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS market_share_percentage,

    ROUND(AVG(f.price_numeric), 2) AS avg_price,
    ROUND(MEDIAN(f.price_numeric), 2) AS median_price,

    ROUND(AVG(f.availability_rate), 4) AS avg_availability_rate,
    ROUND(AVG(f.occupancy_proxy), 4) AS avg_occupancy_proxy,

    ROUND(AVG(f.review_scores_rating), 2) AS avg_review_score,
    SUM(f.detailed_review_count) AS total_reviews,

    ROUND(SUM(f.estimated_revenue_proxy), 2) AS total_revenue_proxy,
    ROUND(AVG(f.estimated_revenue_proxy), 2) AS avg_revenue_proxy,

    SUM(CASE WHEN f.price_numeric IS NULL THEN 1 ELSE 0 END) AS listings_missing_price
FROM fact_listing_market f
LEFT JOIN dim_listing dl
    ON f.listing_key = dl.listing_key
GROUP BY
    dl.room_type
ORDER BY
    listing_count DESC;