-- Top Neighbourhood and Room Type Revenue Proxy
-- Purpose: Identifies neighbourhood-room type combinations with the highest estimated revenue proxy.

SELECT
    dn.neighbourhood,
    dl.room_type,
    COUNT(*) AS listing_count,

    ROUND(AVG(f.price_numeric), 2) AS avg_price,
    ROUND(MEDIAN(f.price_numeric), 2) AS median_price,

    ROUND(AVG(f.availability_rate), 4) AS avg_availability_rate,
    ROUND(AVG(f.occupancy_proxy), 4) AS avg_occupancy_proxy,

    ROUND(SUM(f.estimated_revenue_proxy), 2) AS total_revenue_proxy
FROM fact_listing_market f
LEFT JOIN dim_listing dl
    ON f.listing_key = dl.listing_key
LEFT JOIN dim_neighbourhood dn
    ON f.neighbourhood_key = dn.neighbourhood_key
GROUP BY
    dn.neighbourhood,
    dl.room_type
ORDER BY
    total_revenue_proxy DESC
LIMIT 20;