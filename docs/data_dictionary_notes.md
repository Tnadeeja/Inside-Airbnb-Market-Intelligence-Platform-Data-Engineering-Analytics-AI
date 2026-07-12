
---

# Fill `docs/data_dictionary_notes.md`

Paste this:

```markdown
# Data Dictionary Notes

## Project

Inside Airbnb Market Intelligence Platform — Data Engineering, Analytics & AI

## Purpose

This document explains important raw, cleaned, engineered, and analytical fields used in the project.

It is not a full official Inside Airbnb dictionary. It is a project-specific data dictionary focused on the columns used for cleaning, analysis, warehouse design, and machine learning.

---

## Main Identifier Fields

| Field | Description |
|---|---|
| `id` | Raw listing ID in listings datasets |
| `listing_id` | Standardized listing identifier used across the project |
| `host_id` | Identifier for the Airbnb host |
| `review_id` | Standardized review identifier from detailed reviews |
| `reviewer_id` | Identifier for the reviewer |
| `neighbourhood` | Amsterdam neighbourhood name |
| `neighbourhood_group` | Higher-level neighbourhood grouping, if available |

---

## Listing Fields

| Field | Description |
|---|---|
| `name` | Listing name/title |
| `host_name` | Host display name |
| `room_type` | Type of Airbnb room, such as Entire home/apt or Private room |
| `property_type` | Detailed property type from detailed listings |
| `minimum_nights` | Minimum nights required for booking |
| `license` | Listing license field, where available |
| `latitude` | Listing latitude |
| `longitude` | Listing longitude |

---

## Price Fields

| Field | Description |
|---|---|
| `price` | Raw listing price field |
| `price_numeric` | Cleaned numeric price used for analysis and machine learning |
| `has_valid_price` | Boolean flag showing whether price is available and greater than zero |

Important note:

Listings with missing or invalid prices are excluded from price-based machine learning.

---

## Capacity and Property Features

| Field | Description |
|---|---|
| `accommodates` | Number of guests the listing can accommodate |
| `bathrooms` | Number of bathrooms |
| `bedrooms` | Number of bedrooms |
| `beds` | Number of beds |
| `amenities_count` | Count of amenities parsed from the detailed listings amenities field |

These fields are important for price prediction and property-size analysis.

---

## Calendar Fields

| Field | Description |
|---|---|
| `date` | Calendar date |
| `available` | Raw availability value |
| `available_flag` | Numeric availability flag; 1 means available, 0 means unavailable |
| `unavailable_flag` | Numeric unavailable flag; 1 means unavailable, 0 means available |
| `calendar_days` | Number of calendar days available for a listing |
| `available_days` | Count of available days |
| `unavailable_days` | Count of unavailable days |
| `availability_rate` | Available days divided by calendar days |
| `occupancy_proxy` | Unavailable days divided by calendar days |
| `weekend_availability_rate` | Average availability rate for weekend dates |
| `weekday_availability_rate` | Average availability rate for weekday dates |
| `avg_minimum_nights` | Average minimum night requirement from calendar data |
| `median_minimum_nights` | Median minimum night requirement from calendar data |

Important limitation:

The Amsterdam calendar file used in this project does not contain daily price or adjusted price fields. Therefore, calendar data is used for availability and stay-policy analysis, not actual revenue calculation.

---

## Review Fields

| Field | Description |
|---|---|
| `number_of_reviews` | Summary review count from listings data |
| `reviews_per_month` | Summary review frequency |
| `review_date` | Parsed review date |
| `detailed_review_count` | Count of detailed reviews per listing |
| `unique_reviewer_count` | Count of unique reviewers per listing |
| `first_review_date` | First detailed review date |
| `last_review_date` | Latest detailed review date |
| `detailed_reviews_last_365d` | Number of detailed reviews in the last 365 days from the snapshot date |
| `reviews_with_comments` | Count of reviews with written comments |
| `comment_coverage_rate` | Share of detailed reviews with written comments |
| `average_comment_length` | Average length of review comments |
| `median_comment_length` | Median length of review comments |
| `avg_reviews_per_year` | Average review count per active review year |

---

## Review Score Fields

| Field | Description |
|---|---|
| `review_scores_rating` | Overall review rating |
| `review_scores_accuracy` | Accuracy score |
| `review_scores_cleanliness` | Cleanliness score |
| `review_scores_checkin` | Check-in score |
| `review_scores_communication` | Communication score |
| `review_scores_location` | Location score |
| `review_scores_value` | Value score |

These fields are used for review quality analysis and machine learning.

---

## Host Fields

| Field | Description |
|---|---|
| `host_since` | Date when the host joined Airbnb |
| `host_is_superhost` | Whether the host is marked as superhost |
| `host_identity_verified` | Whether host identity is verified |
| `calculated_host_listings_count` | Number of listings associated with the host |
| `host_portfolio_segment` | Engineered host segment based on host listing count |

Host portfolio segments:

| Segment | Meaning |
|---|---|
| `Unknown Host` | Missing host information |
| `Single-listing Host` | Host has one listing |
| `Small Portfolio Host` | Host has 2 to 5 listings |
| `Medium Portfolio Host` | Host has 6 to 20 listings |
| `Large Portfolio Host` | Host has more than 20 listings |

---

## Availability Segment

| Segment | Meaning |
|---|---|
| `Unknown` | Missing availability rate |
| `Low Availability` | Availability rate is 10% or below |
| `Medium Availability` | Availability rate is above 10% and up to 50% |
| `High Availability` | Availability rate is above 50% |

This helps describe listing availability behavior.

---

## Neighbourhood Metrics

| Field | Description |
|---|---|
| `neighbourhood_listing_count` | Number of listings in the neighbourhood |
| `neighbourhood_avg_price` | Average listing price in the neighbourhood |
| `neighbourhood_median_price` | Median listing price in the neighbourhood |
| `neighbourhood_avg_availability_rate` | Average availability rate in the neighbourhood |
| `neighbourhood_avg_occupancy_proxy` | Average occupancy proxy in the neighbourhood |
| `neighbourhood_total_reviews` | Total review count in the neighbourhood |

Important ML note:

Neighbourhood median price is useful as a market context feature. In a strict production ML workflow, neighbourhood-level target-derived features should be calculated using training data only to avoid leakage risk.

---

## Warehouse Keys

| Field | Description |
|---|---|
| `listing_key` | Surrogate key for listing dimension |
| `host_key` | Surrogate key for host dimension |
| `neighbourhood_key` | Surrogate key for neighbourhood dimension |
| `fact_key` | Surrogate key for fact table row |

Special handling:

Missing host IDs are assigned to an Unknown Host record with:

```text
host_key = -1