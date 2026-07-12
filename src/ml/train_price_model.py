"""
Reusable machine learning training script for Airbnb price prediction.

This module trains regression models to predict listing price using the final
listing master dataset. It saves model evaluation results, feature importance,
prediction errors, and the final Random Forest model package.

Run from project root:

    python -m src.ml.train_price_model
"""

from pathlib import Path
from typing import Dict, List, Tuple

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import (
    PROCESSED_CITY_DIR,
    MODELS_DIR,
    REPORTS_DIR,
)


ML_REPORTS_DIR = REPORTS_DIR / "machine_learning"
ML_FIGURES_DIR = REPORTS_DIR / "figures" / "machine_learning"


RANDOM_STATE = 42
TARGET_COLUMN = "price_numeric"


NUMERIC_FEATURE_CANDIDATES = [
    "minimum_nights",
    "number_of_reviews",
    "reviews_per_month",
    "calculated_host_listings_count",
    "availability_365",
    "availability_rate",
    "occupancy_proxy",
    "weekend_availability_rate",
    "weekday_availability_rate",
    "accommodates",
    "bathrooms",
    "bedrooms",
    "beds",
    "amenities_count",
    "review_scores_rating",
    "review_scores_cleanliness",
    "review_scores_location",
    "review_scores_value",
    "detailed_review_count",
    "unique_reviewer_count",
    "detailed_reviews_last_365d",
    "avg_reviews_per_year",
    "neighbourhood_median_price",
    "neighbourhood_avg_occupancy_proxy",
]


CATEGORICAL_FEATURE_CANDIDATES = [
    "room_type",
    "property_type",
    "host_is_superhost",
    "host_identity_verified",
    "instant_bookable",
    "host_portfolio_segment",
    "availability_segment",
    "neighbourhood",
]


LEAKAGE_FEATURES = [
    "price_numeric",
    "estimated_revenue_proxy",
    "unavailable_days_numeric",
]


def get_listing_master_path() -> Path:
    """
    Return the preferred final listing master parquet path.
    """
    src_listing_master_path = PROCESSED_CITY_DIR / "listing_master_final_from_src.parquet"
    notebook_listing_master_path = PROCESSED_CITY_DIR / "listing_master_final.parquet"

    if src_listing_master_path.exists():
        return src_listing_master_path

    if notebook_listing_master_path.exists():
        return notebook_listing_master_path

    raise FileNotFoundError(
        "Final listing master parquet file not found. "
        "Run the listing master builder first."
    )


def load_listing_master() -> pd.DataFrame:
    """
    Load final listing master table.
    """
    listing_master_path = get_listing_master_path()
    print(f"Loading listing master from: {listing_master_path}")

    return pd.read_parquet(listing_master_path)


def prepare_ml_dataset(
    listing_master: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.Series, List[str], List[str], pd.DataFrame]:
    """
    Prepare ML features and target.

    Returns:
        X: Feature DataFrame
        y: Target Series
        numeric_features: Selected numeric feature names
        categorical_features: Selected categorical feature names
        ml_df: Filtered ML dataframe
    """
    ml_df = listing_master.copy()

    ml_df[TARGET_COLUMN] = pd.to_numeric(ml_df[TARGET_COLUMN], errors="coerce")

    ml_df = ml_df[
        ml_df[TARGET_COLUMN].notna()
        & (ml_df[TARGET_COLUMN] > 0)
    ].copy()

    numeric_features = [
        feature
        for feature in NUMERIC_FEATURE_CANDIDATES
        if feature in ml_df.columns and feature not in LEAKAGE_FEATURES
    ]

    categorical_features = [
        feature
        for feature in CATEGORICAL_FEATURE_CANDIDATES
        if feature in ml_df.columns and feature not in LEAKAGE_FEATURES
    ]

    for column in numeric_features:
        ml_df[column] = pd.to_numeric(ml_df[column], errors="coerce")

    usable_categorical_features = []

    for column in categorical_features:
        missing_rate = ml_df[column].isna().mean()

        if missing_rate < 1.0:
            ml_df[column] = (
                ml_df[column]
                .astype("object")
                .where(ml_df[column].notna(), "Missing")
                .astype(str)
            )
            usable_categorical_features.append(column)

    categorical_features = usable_categorical_features

    selected_features = numeric_features + categorical_features

    X = ml_df[selected_features].copy()
    y = ml_df[TARGET_COLUMN].copy()

    print("\nML dataset prepared.")
    print(f"Rows used for ML: {len(ml_df)}")
    print(f"Numeric features: {len(numeric_features)}")
    print(f"Categorical features: {len(categorical_features)}")
    print(f"Total input features before encoding: {len(selected_features)}")

    return X, y, numeric_features, categorical_features, ml_df


def build_preprocessor(
    numeric_features: List[str],
    categorical_features: List[str],
) -> ColumnTransformer:
    """
    Build preprocessing pipeline for numeric and categorical features.
    """
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    try:
        one_hot_encoder = OneHotEncoder(
            handle_unknown="ignore",
            sparse_output=False,
        )
    except TypeError:
        one_hot_encoder = OneHotEncoder(
            handle_unknown="ignore",
            sparse=False,
        )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="Missing")),
            ("onehot", one_hot_encoder),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, numeric_features),
            ("categorical", categorical_transformer, categorical_features),
        ]
    )

    return preprocessor


def build_models(preprocessor: ColumnTransformer) -> Dict[str, Pipeline]:
    """
    Build model pipelines.
    """
    models = {
        "Dummy Median Baseline": DummyRegressor(strategy="median"),
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=100,
            max_depth=12,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "Gradient Boosting Regressor": GradientBoostingRegressor(
            n_estimators=150,
            learning_rate=0.05,
            max_depth=3,
            random_state=RANDOM_STATE,
        ),
    }

    model_pipelines = {}

    for model_name, model in models.items():
        model_pipelines[model_name] = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model),
            ]
        )

    return model_pipelines


def evaluate_model(
    model_name: str,
    y_true: pd.Series,
    y_pred: np.ndarray,
) -> dict:
    """
    Evaluate regression predictions.
    """
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    r2 = float(r2_score(y_true, y_pred))

    return {
        "model_name": model_name,
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2_score": round(r2, 4),
    }


def train_and_evaluate_models(
    model_pipelines: Dict[str, Pipeline],
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> Tuple[pd.DataFrame, Dict[str, Pipeline], Dict[str, np.ndarray]]:
    """
    Train and evaluate all model pipelines.
    """
    results = []
    trained_models = {}
    predictions = {}

    for model_name, model_pipeline in model_pipelines.items():
        print(f"Training model: {model_name}")

        model_pipeline.fit(X_train, y_train)

        y_pred = model_pipeline.predict(X_test)

        results.append(
            evaluate_model(
                model_name=model_name,
                y_true=y_test,
                y_pred=y_pred,
            )
        )

        trained_models[model_name] = model_pipeline
        predictions[model_name] = y_pred

    model_results = (
        pd.DataFrame(results)
        .sort_values("rmse", ascending=True)
        .reset_index(drop=True)
    )

    return model_results, trained_models, predictions


def get_processed_feature_names(
    trained_pipeline: Pipeline,
    numeric_features: List[str],
    categorical_features: List[str],
) -> List[str]:
    """
    Get feature names after preprocessing.
    """
    preprocessor = trained_pipeline.named_steps["preprocessor"]

    categorical_pipeline = preprocessor.named_transformers_["categorical"]
    onehot_encoder = categorical_pipeline.named_steps["onehot"]

    categorical_feature_names = onehot_encoder.get_feature_names_out(
        categorical_features
    ).tolist()

    return numeric_features + categorical_feature_names


def create_feature_importance(
    random_forest_pipeline: Pipeline,
    numeric_features: List[str],
    categorical_features: List[str],
) -> pd.DataFrame:
    """
    Create Random Forest feature importance table.
    """
    model = random_forest_pipeline.named_steps["model"]

    processed_feature_names = get_processed_feature_names(
        trained_pipeline=random_forest_pipeline,
        numeric_features=numeric_features,
        categorical_features=categorical_features,
    )

    feature_importance = pd.DataFrame(
        {
            "feature": processed_feature_names,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    return feature_importance


def create_prediction_results(
    ml_df: pd.DataFrame,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    y_pred: np.ndarray,
) -> pd.DataFrame:
    """
    Create prediction results and residual error table.
    """
    preferred_columns = [
        "listing_id",
        "name",
        "room_type",
        "neighbourhood",
        "host_portfolio_segment",
        "price_numeric",
        "bedrooms",
        "bathrooms",
        "beds",
        "accommodates",
        "review_scores_value",
        "minimum_nights",
    ]

    existing_columns = [
        column for column in preferred_columns if column in ml_df.columns
    ]

    prediction_results = ml_df.loc[X_test.index, existing_columns].copy()

    prediction_results["actual_price"] = y_test.values
    prediction_results["predicted_price"] = y_pred
    prediction_results["prediction_error"] = (
        prediction_results["actual_price"] - prediction_results["predicted_price"]
    )
    prediction_results["absolute_error"] = prediction_results["prediction_error"].abs()

    round_columns = [
        "actual_price",
        "predicted_price",
        "prediction_error",
        "absolute_error",
    ]

    for column in round_columns:
        prediction_results[column] = prediction_results[column].round(2)

    return prediction_results


def create_final_ml_summary(
    model_results: pd.DataFrame,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    input_feature_count: int,
    processed_feature_count: int,
) -> pd.DataFrame:
    """
    Create final ML summary table.
    """
    best_model = model_results.iloc[0]

    baseline_rmse = model_results[
        model_results["model_name"] == "Dummy Median Baseline"
    ]["rmse"].iloc[0]

    rmse_improvement = baseline_rmse - best_model["rmse"]
    rmse_improvement_percentage = (rmse_improvement / baseline_rmse) * 100

    return pd.DataFrame(
        [
            {"metric": "best_model", "value": best_model["model_name"]},
            {"metric": "best_model_mae", "value": best_model["mae"]},
            {"metric": "best_model_rmse", "value": best_model["rmse"]},
            {"metric": "best_model_r2", "value": best_model["r2_score"]},
            {"metric": "baseline_rmse", "value": baseline_rmse},
            {
                "metric": "rmse_improvement_vs_baseline",
                "value": round(rmse_improvement, 2),
            },
            {
                "metric": "rmse_improvement_percentage",
                "value": round(rmse_improvement_percentage, 2),
            },
            {"metric": "training_rows", "value": X_train.shape[0]},
            {"metric": "testing_rows", "value": X_test.shape[0]},
            {"metric": "input_features_before_encoding", "value": input_feature_count},
            {
                "metric": "processed_features_after_encoding",
                "value": processed_feature_count,
            },
        ]
    )


def save_plots(
    prediction_results: pd.DataFrame,
    feature_importance: pd.DataFrame,
) -> None:
    """
    Save key ML diagnostic plots.
    """
    ML_FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.scatter(
        prediction_results["actual_price"],
        prediction_results["predicted_price"],
        alpha=0.4,
    )
    plt.title("Actual vs Predicted Price - Random Forest")
    plt.xlabel("Actual Price")
    plt.ylabel("Predicted Price")
    plt.tight_layout()
    plt.savefig(
        ML_FIGURES_DIR / "actual_vs_predicted_price_random_forest_from_src.png",
        dpi=300,
    )
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.hist(prediction_results["prediction_error"], bins=50)
    plt.title("Prediction Error Distribution - Random Forest")
    plt.xlabel("Prediction Error")
    plt.ylabel("Listing Count")
    plt.tight_layout()
    plt.savefig(
        ML_FIGURES_DIR / "prediction_error_distribution_random_forest_from_src.png",
        dpi=300,
    )
    plt.close()

    top_features = feature_importance.head(15).sort_values(
        "importance",
        ascending=True,
    )

    plt.figure(figsize=(10, 7))
    plt.barh(top_features["feature"], top_features["importance"])
    plt.title("Top 15 Random Forest Feature Importances")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.tight_layout()
    plt.savefig(
        ML_FIGURES_DIR / "random_forest_top_feature_importance_from_src.png",
        dpi=300,
    )
    plt.close()


def save_model_package(
    random_forest_pipeline: Pipeline,
    numeric_features: List[str],
    categorical_features: List[str],
    selected_features: List[str],
    model_results: pd.DataFrame,
) -> None:
    """
    Save final Random Forest model package.
    """
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    final_model_package = {
        "model_pipeline": random_forest_pipeline,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "selected_features": selected_features,
        "target_column": TARGET_COLUMN,
        "model_name": "Random Forest Regressor",
        "performance": model_results[
            model_results["model_name"] == "Random Forest Regressor"
        ].iloc[0].to_dict(),
    }

    model_output_path = MODELS_DIR / "random_forest_price_prediction_model_from_src.joblib"

    joblib.dump(final_model_package, model_output_path)

    print(f"Model package saved to: {model_output_path}")


def run_ml_training() -> None:
    """
    Run the full reusable ML training workflow.
    """
    ML_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ML_FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    listing_master = load_listing_master()

    X, y, numeric_features, categorical_features, ml_df = prepare_ml_dataset(
        listing_master
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
    )

    print("\nTrain/test split complete.")
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")

    preprocessor = build_preprocessor(
        numeric_features=numeric_features,
        categorical_features=categorical_features,
    )

    model_pipelines = build_models(preprocessor)

    model_results, trained_models, predictions = train_and_evaluate_models(
        model_pipelines=model_pipelines,
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
    )

    print("\nModel comparison:")
    print(model_results)

    random_forest_pipeline = trained_models["Random Forest Regressor"]
    random_forest_predictions = predictions["Random Forest Regressor"]

    feature_importance = create_feature_importance(
        random_forest_pipeline=random_forest_pipeline,
        numeric_features=numeric_features,
        categorical_features=categorical_features,
    )

    prediction_results = create_prediction_results(
        ml_df=ml_df,
        X_test=X_test,
        y_test=y_test,
        y_pred=random_forest_predictions,
    )

    processed_feature_count = len(
        get_processed_feature_names(
            trained_pipeline=random_forest_pipeline,
            numeric_features=numeric_features,
            categorical_features=categorical_features,
        )
    )

    ml_final_summary = create_final_ml_summary(
        model_results=model_results,
        X_train=X_train,
        X_test=X_test,
        input_feature_count=X.shape[1],
        processed_feature_count=processed_feature_count,
    )

    residual_summary = pd.DataFrame(
        [
            {
                "metric": "mean_error",
                "value": round(prediction_results["prediction_error"].mean(), 2),
            },
            {
                "metric": "median_error",
                "value": round(prediction_results["prediction_error"].median(), 2),
            },
            {
                "metric": "mean_absolute_error",
                "value": round(prediction_results["absolute_error"].mean(), 2),
            },
            {
                "metric": "median_absolute_error",
                "value": round(prediction_results["absolute_error"].median(), 2),
            },
            {
                "metric": "max_absolute_error",
                "value": round(prediction_results["absolute_error"].max(), 2),
            },
            {
                "metric": "prediction_count",
                "value": len(prediction_results),
            },
        ]
    )

    print("\nFinal ML summary:")
    print(ml_final_summary)

    print("\nTop 15 feature importances:")
    print(feature_importance.head(15))

    print("\nResidual summary:")
    print(residual_summary)

    model_results.to_csv(
        ML_REPORTS_DIR / "model_comparison_from_src.csv",
        index=False,
    )

    ml_final_summary.to_csv(
        ML_REPORTS_DIR / "ml_final_summary_from_src.csv",
        index=False,
    )

    feature_importance.to_csv(
        ML_REPORTS_DIR / "random_forest_feature_importance_from_src.csv",
        index=False,
    )

    prediction_results.to_csv(
        ML_REPORTS_DIR / "random_forest_prediction_results_from_src.csv",
        index=False,
    )

    residual_summary.to_csv(
        ML_REPORTS_DIR / "random_forest_residual_summary_from_src.csv",
        index=False,
    )

    save_plots(
        prediction_results=prediction_results,
        feature_importance=feature_importance,
    )

    save_model_package(
        random_forest_pipeline=random_forest_pipeline,
        numeric_features=numeric_features,
        categorical_features=categorical_features,
        selected_features=numeric_features + categorical_features,
        model_results=model_results,
    )

    print("\nReusable ML training completed successfully.")


if __name__ == "__main__":
    run_ml_training()