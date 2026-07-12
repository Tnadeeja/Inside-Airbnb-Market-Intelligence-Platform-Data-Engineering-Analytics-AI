# Assumptions Log

## Project

Inside Airbnb Market Intelligence Platform — Data Engineering, Analytics & AI

## Purpose

This document records the main assumptions used during data engineering, analytics, statistical analysis, and machine learning.

These assumptions are documented to make the project more transparent and reproducible.

---

## Assumption 001: Summary Listings as Base Listing Universe

**Assumption:**  
The `listings.csv` summary listings dataset is used as the main listing universe.

**Reason:**  
It contains 10,465 unique listings and aligns with the calendar dataset listing coverage.

**Impact:**  
This preserves broader market coverage, even though some listings may not have detailed metadata from `listings.csv.gz`.

---

## Assumption 002: Calendar Data Represents Availability Status

**Assumption:**  
The `available` field in the calendar dataset can be used to calculate listing availability.

**Reason:**  
The calendar file provides daily availability values for each listing.

**Impact:**  
This allows calculation of availability rate, unavailable days, weekend availability, and weekday availability.

---

## Assumption 003: Occupancy Proxy Uses Unavailable Days

**Assumption:**  
Unavailable days are used as an occupancy proxy.

```text
occupancy_proxy = unavailable_days / calendar_days