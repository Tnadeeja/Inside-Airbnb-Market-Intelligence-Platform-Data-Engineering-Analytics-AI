# Machine Learning Model Card

## Project

Inside Airbnb Market Intelligence Platform — Data Engineering, Analytics & AI

## Model Name

Random Forest Price Prediction Model

## Model Purpose

The purpose of this model is to estimate Airbnb listing prices in Amsterdam using listing, host, review, availability, and neighbourhood features.

The model is designed for analytical and decision-support purposes. It is not intended to be used as a fully automated pricing engine.

## Prediction Target

The model predicts:

```text
price_numeric
```

This represents the cleaned listing price from the summary listings dataset.

## Problem Type

This is a supervised machine learning regression problem.

The model predicts a continuous numeric value:

```
Airbnb listing price
```

## Dataset Scope

City:

```
Amsterdam, North Holland, The Netherlands
```

Snapshot date:

```
2026-06-15
```

Rows used for ML:

```
6,471 listings with valid positive price values
```

Excluded rows:

```
3,994 listings with missing or invalid price values
```

## Input Features

The model uses selected numeric and categorical features.

### Numeric Feature Examples

- Minimum nights
- Number of reviews
- Reviews per month
- Availability 365
- Availability rate
- Occupancy proxy
- Weekend availability rate
- Weekday availability rate
- Accommodates
- Bathrooms
- Bedrooms
- Beds
- Amenities count
- Review scores
- Detailed review count
- Unique reviewer count
- Reviews in the last 365 days
- Average reviews per year
- Neighbourhood median price
- Neighbourhood average occupancy proxy

### Categorical Feature Examples

- Room type
- Property type
- Host is superhost
- Host identity verified
- Host portfolio segment
- Availability segment
- Neighbourhood

## Features Excluded to Avoid Target Leakage

The following fields are excluded from model training:

```
price_numeric
estimated_revenue_proxy
unavailable_days_numeric
```

Important reason:

```
estimated_revenue_proxy = price_numeric × unavailable_days
```

Because estimated revenue proxy directly uses price, including it would leak the target into the model.

## Preprocessing

The ML pipeline applies:

- Median imputation for numeric features
- Standard scaling for numeric features
- Missing value handling for categorical features
- One-hot encoding for categorical features

Input feature count before encoding:

```
31
```

Processed feature count after encoding:

```
121
```

## Train/Test Split

The data is split into:

```
80% training data
20% testing data
```

Training rows:

```
5,176
```

Testing rows:

```
1,295
```

Random state:

```
42
```

## Models Compared

The following models were trained and compared:

- Dummy Median Baseline
- Linear Regression
- Ridge Regression
- Random Forest Regressor
- Gradient Boosting Regressor

## Final Selected Model

The selected model is:

```
Random Forest Regressor
```

Reason for selection:

```
The Random Forest Regressor achieved the lowest RMSE and highest R² score among the tested models.
```

## Model Performance

Final Random Forest performance:

MetricValueMAE88.40RMSE147.30R² Score0.5009

Baseline model:

MetricValueDummy Median Baseline RMSE213.50

Improvement over baseline:

MetricValueRMSE Improvement66.20RMSE Improvement Percentage31.01%

## Performance Interpretation

The Random Forest model reduced RMSE by 31.01% compared with the dummy median baseline.

This shows that the selected listing, host, review, availability, and neighbourhood features contain useful predictive signals for estimating Airbnb prices.

However, the model explains about half of the price variation. This means price prediction remains difficult because important pricing drivers are not fully captured in the dataset.

## Feature Importance Summary

The most important predictive signals include:

- Bedrooms
- Review scores value
- Minimum nights
- Beds
- Bathrooms
- Neighbourhood context
- Average reviews per year
- Amenities count
- Reviews per month
- Accommodates
- Room type
- Occupancy proxy
- Availability rate

Important interpretation:

```
Feature importance shows predictive value, not causation.
```

For example, the model uses bedrooms as a strong signal for price, but this does not mean bedrooms alone cause price changes.

## Residual Analysis

Residual analysis shows that the model performs better for common price ranges and struggles more with unusual or luxury listings.

Residual summary:

MetricValueMean Error-9.84Median Error-19.76Mean Absolute Error88.40Median Absolute Error58.41Maximum Absolute Error1578.65Prediction Count1,295

The negative mean error indicates that the model slightly overpredicts on average.

Large errors are mainly found in unusual or premium listings such as:

- Luxury houseboats
- Historical sailing ships
- Canal-view properties
- High-end townhouses
- Unique premium properties

## Known Limitations

The model has several important limitations:

- The model is trained on one Amsterdam snapshot only.
- Listings with missing or invalid price values are excluded.
- Price is right-skewed and contains high-value outliers.
- The model does not include photos, interior quality, exact view, design quality, or street-level desirability.
- The model does not include seasonality, event demand, or confirmed booking data.
- Calendar unavailable days may include booked days or host-blocked days.
- Estimated revenue proxy is excluded to avoid target leakage.
- Neighbourhood median price is useful for market context, but should be calculated carefully in strict production ML workflows.

## Intended Use

This model can be used for:

- Approximate price estimation
- Market analysis
- Feature importance explanation
- Understanding pricing patterns
- Supporting business intelligence dashboards
- Demonstrating ML workflow and model explainability

## Not Intended For

This model should not be used for:

- Fully automated pricing decisions
- Legal, financial, or regulatory decisions
- Exact revenue forecasting
- Replacing professional market analysis
- Making decisions about individual hosts or guests without human review

## Responsible AI and Fairness Considerations

The model is used for analytical purposes only.

Potential risks include:

- Overinterpreting predictions as exact prices
- Treating proxy revenue as real revenue
- Underestimating unique luxury listings
- Bias from missing price values
- Bias from historical host pricing behavior
- Limited generalization outside Amsterdam

To reduce these risks, the project clearly documents assumptions, limitations, target leakage controls, and model interpretation boundaries.

## Reproducibility

The reusable ML training script is:

```
python -m src.ml.train_price_model
```

This script creates:

- Model comparison report
- Final ML summary
- Random Forest feature importance
- Prediction results
- Residual summary
- Diagnostic plots
- Final model package

## Model Artifact

The trained model package is saved locally as:

```
models/random_forest_price_prediction_model_from_src.joblib
```

Model artifacts are not committed to Git because they are generated outputs and can be recreated from the pipeline.

## Final Model Conclusion

The Random Forest Regressor provides a useful and explainable baseline for Airbnb price prediction in Amsterdam.

The model performs significantly better than a dummy baseline and identifies meaningful pricing signals related to property size, review value, neighbourhood context, availability, and room type.

However, because Airbnb price is influenced by many qualitative and time-sensitive factors, the model should be treated as a decision-support tool rather than a final pricing system.
