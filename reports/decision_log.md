# Engineering Decision Log

## Decision 001: Base Listing Table Selection

**Decision:** Use `summary_listings` as the base listing universe and enrich it with fields from `detailed_listings`.

**Options considered:**
1. Use `detailed_listings` as the base table because it has more attributes.
2. Use `summary_listings` as the base table because it has broader listing coverage.
3. Inner join both tables and keep only matching listings.

**Chosen approach:** Option 2.

**Reasoning:**  
The summary listings table contains 10,465 unique listings, while detailed listings contains 10,369. Calendar data also contains 10,465 unique listing IDs, which aligns with the summary listings table. Using summary listings as the base preserves the broadest listing coverage and avoids dropping 96 listings that still have calendar records.

**Trade-off:**  
Some listings will not have detailed metadata such as amenities, descriptions, or host profile fields. These missing enriched fields will be retained as nulls and documented during transformation.

**Impact:**  
This approach improves coverage for market-level analysis while still allowing richer feature engineering for listings that have detailed metadata.

## Decision 002: Calendar Dataset Usage

**Decision:** Use the calendar dataset for availability and stay-policy analysis, not direct pricing analysis.

**Reasoning:**  
The Amsterdam calendar snapshot contains listing_id, date, available, minimum_nights, and maximum_nights. It does not contain price or adjusted_price fields.

**Trade-off:**  
Daily price trends, weekend price premium, and direct calendar-based revenue cannot be calculated from this calendar file.

**Impact:**  
Calendar-derived features will focus on calendar_days, available_days, unavailable_days, availability_rate, occupancy_proxy, weekend availability, weekday availability, and stay-policy metrics.