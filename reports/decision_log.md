# Engineering Decision Log

## Decision 001: Base Listing Table Selection

**Decision:** Use `summary_listings` as the base listing universe and enrich it with fields from `detailed_listings`.

**Reasoning:**  
The summary listings table contains 10,465 unique listings, while detailed listings contains 10,369. Calendar data also contains 10,465 unique listing IDs, which aligns with the summary listings table.

**Trade-off:**  
Some listings will not have detailed metadata such as amenities, descriptions, or host profile fields.

**Impact:**  
This approach preserves market coverage while still allowing rich analysis for listings with detailed metadata.

---

## Decision 002: Calendar Dataset Usage

**Decision:** Use the calendar dataset for availability and stay-policy analysis, not direct pricing analysis.

**Reasoning:**  
The Amsterdam calendar snapshot contains `listing_id`, `date`, `available`, `minimum_nights`, and `maximum_nights`. It does not contain `price` or `adjusted_price` fields.

**Trade-off:**  
Daily price trends, weekend price premium, and direct calendar-based revenue cannot be calculated from the calendar file.

**Impact:**  
Calendar-derived features will focus on availability rate, occupancy proxy, weekend/weekday availability, and stay-policy metrics.

## Decision 003: Unknown Host Dimension Record

**Decision:** Add an Unknown Host record to `dim_host` using `host_key = -1`.

**Reasoning:**  
During star schema validation, 96 fact rows had missing host_id values and therefore could not join to a known host dimension record.

**Trade-off:**  
The original host identity for these 96 listings remains unknown. However, assigning them to an Unknown Host record preserves all listing records and maintains warehouse referential consistency.

**Impact:**  
The fact table has no missing host keys, and records with incomplete host metadata remain visible for analysis instead of being dropped.