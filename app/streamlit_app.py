"""
Streamlit dashboard for the Inside Airbnb Market Intelligence Platform.

Run from project root:

    streamlit run app/streamlit_app.py
"""

from pathlib import Path

import pandas as pd
import streamlit as st


# ---------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="Inside Airbnb Market Intelligence",
    page_icon="🏠",
    layout="wide",
)


# ---------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REPORTS_DIR = PROJECT_ROOT / "reports"
ANALYTICS_DIR = REPORTS_DIR / "analytics_outputs"
ML_DIR = REPORTS_DIR / "machine_learning"
FIGURES_DIR = REPORTS_DIR / "figures"
ML_FIGURES_DIR = FIGURES_DIR / "machine_learning"
DOCS_DIR = PROJECT_ROOT / "docs"


# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------

@st.cache_data
def load_csv_if_exists(*paths):
    """
    Load the first existing CSV file from a list of possible paths.
    """
    for path in paths:
        if Path(path).exists():
            return pd.read_csv(path)

    return pd.DataFrame()


def show_missing_message(file_name: str):
    """
    Show a helpful message when an expected file is missing.
    """
    st.warning(
        f"Could not find `{file_name}`. "
        "Run `python -m src.pipeline_runner` and `python -m src.ml.train_price_model` first."
    )


def format_number(value):
    """
    Format numbers for dashboard KPI display.
    """
    if pd.isna(value):
        return "N/A"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return value

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"{value:,.0f}"

    if value % 1 == 0:
        return f"{value:,.0f}"

    return f"{value:,.2f}"


def read_markdown_file(path: Path) -> str:
    """
    Read markdown file safely.
    """
    if path.exists():
        return path.read_text(encoding="utf-8")

    return "Documentation file not found."


# ---------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------

market_overview = load_csv_if_exists(
    ANALYTICS_DIR / "market_overview_from_src.csv",
    ANALYTICS_DIR / "market_overview.csv",
)

room_type_summary = load_csv_if_exists(
    ANALYTICS_DIR / "room_type_summary_from_src.csv",
    ANALYTICS_DIR / "room_type_summary.csv",
)

neighbourhood_summary = load_csv_if_exists(
    ANALYTICS_DIR / "neighbourhood_summary_from_src.csv",
    ANALYTICS_DIR / "neighbourhood_summary.csv",
)

host_portfolio_summary = load_csv_if_exists(
    ANALYTICS_DIR / "host_portfolio_summary_from_src.csv",
    ANALYTICS_DIR / "host_portfolio_summary.csv",
)

review_score_summary = load_csv_if_exists(
    ANALYTICS_DIR / "review_score_summary_from_src.csv",
    ANALYTICS_DIR / "review_score_summary.csv",
)

model_comparison = load_csv_if_exists(
    ML_DIR / "model_comparison_from_src.csv",
    ML_DIR / "model_comparison.csv",
)

ml_final_summary = load_csv_if_exists(
    ML_DIR / "ml_final_summary_from_src.csv",
    ML_DIR / "ml_final_summary.csv",
)

feature_importance = load_csv_if_exists(
    ML_DIR / "random_forest_feature_importance_from_src.csv",
    ML_DIR / "random_forest_feature_importance.csv",
)

residual_summary = load_csv_if_exists(
    ML_DIR / "random_forest_residual_summary_from_src.csv",
    ML_DIR / "random_forest_residual_summary.csv",
)


# ---------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Executive Overview",
        "Room Type Insights",
        "Neighbourhood Insights",
        "Host & Review Insights",
        "ML Price Prediction",
        "AI Innovation & Limitations",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Project:** Inside Airbnb Market Intelligence Platform")
st.sidebar.markdown("**City:** Amsterdam")
st.sidebar.markdown("**Snapshot:** 2026-06-15")

# Neighbourhood filter (safe: uses loaded CSV if available)
if not neighbourhood_summary.empty:
    neighbourhood_names = ["All"] + sorted(neighbourhood_summary["neighbourhood"].unique().tolist())
else:
    neighbourhood_names = ["All"]

neighbourhood = st.sidebar.selectbox("Neighbourhood", neighbourhood_names)


# ---------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------

st.title("🏠 Inside Airbnb Market Intelligence Platform")
st.caption("Data Engineering • Analytics • Statistics • Machine Learning • AI Innovation")


# ---------------------------------------------------------------------
# Page 1: Executive Overview
# ---------------------------------------------------------------------

if page == "Executive Overview":
    st.header("Executive Overview")

    st.markdown(
        """
        This dashboard summarizes the Amsterdam Airbnb market using generated outputs from the
        end-to-end data engineering and analytics pipeline.
        """
    )

    if market_overview.empty:
        show_missing_message("market_overview_from_src.csv")
    else:
        # If a neighbourhood is selected, prefer neighbourhood-level summary for KPIs
        if neighbourhood != "All" and not neighbourhood_summary.empty:
            n_row = neighbourhood_summary[neighbourhood_summary["neighbourhood"] == neighbourhood]
            if not n_row.empty:
                n_row = n_row.iloc[0]
                # map neighbourhood summary fields into the same keys used by market_overview
                row = {
                    "total_listings": n_row.get("listing_count"),
                    "total_known_hosts": None,
                    "total_neighbourhoods": 1,
                    "median_listing_price": n_row.get("median_price"),
                    "avg_availability_rate": n_row.get("avg_availability_rate"),
                    "avg_occupancy_proxy": n_row.get("avg_occupancy_proxy"),
                    "listings_with_reviews": None,
                    "total_estimated_revenue_proxy": n_row.get("total_estimated_revenue_proxy"),
                }
            else:
                row = market_overview.iloc[0]
        else:
            row = market_overview.iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Listings", format_number(row.get("total_listings")))
        col2.metric("Known Hosts", format_number(row.get("total_known_hosts")))
        col3.metric("Neighbourhoods", format_number(row.get("total_neighbourhoods")))
        col4.metric("Median Price", format_number(row.get("median_listing_price")))

        col5, col6, col7, col8 = st.columns(4)

        col5.metric("Avg Availability Rate", format_number(row.get("avg_availability_rate")))
        col6.metric("Avg Occupancy Proxy", format_number(row.get("avg_occupancy_proxy")))
        col7.metric("Listings With Reviews", format_number(row.get("listings_with_reviews")))
        col8.metric(
            "Revenue Proxy",
            format_number(row.get("total_estimated_revenue_proxy")),
        )

        st.subheader("Market Overview Table")
        if neighbourhood != "All" and not neighbourhood_summary.empty:
            st.dataframe(neighbourhood_summary[neighbourhood_summary["neighbourhood"] == neighbourhood], use_container_width=True)
        else:
            st.dataframe(market_overview, use_container_width=True)

    st.subheader("Important Interpretation Notes")

    st.info(
        """
        Occupancy proxy is calculated using unavailable days. It is not confirmed occupancy,
        because unavailable dates may include both booked dates and host-blocked dates.
        """
    )

    st.info(
        """
        Estimated revenue proxy is calculated as price × unavailable days.
        It is not actual confirmed revenue.
        """
    )


# ---------------------------------------------------------------------
# Page 2: Room Type Insights
# ---------------------------------------------------------------------

elif page == "Room Type Insights":
    st.header("Room Type Insights")

    if room_type_summary.empty:
        show_missing_message("room_type_summary_from_src.csv")
    else:
        st.subheader("Room Type Summary")
        st.dataframe(room_type_summary, use_container_width=True)

        chart_data = room_type_summary.set_index("room_type")

        st.subheader("Listing Count by Room Type")
        st.bar_chart(chart_data["listing_count"])

        if "median_price" in chart_data.columns:
            st.subheader("Median Price by Room Type")
            st.bar_chart(chart_data["median_price"])

        if "avg_occupancy_proxy" in chart_data.columns:
            st.subheader("Average Occupancy Proxy by Room Type")
            st.bar_chart(chart_data["avg_occupancy_proxy"])

        st.markdown(
            """
            **Business interpretation:**  
            Room type is one of the strongest market segmentation variables. It affects supply,
            pricing, availability behavior, and model prediction patterns.
            """
        )


# ---------------------------------------------------------------------
# Page 3: Neighbourhood Insights
# ---------------------------------------------------------------------

elif page == "Neighbourhood Insights":
    st.header("Neighbourhood Insights")

    if neighbourhood_summary.empty:
        show_missing_message("neighbourhood_summary_from_src.csv")
    else:
        st.subheader("Neighbourhood Summary")
        if neighbourhood != "All":
            filtered = neighbourhood_summary[neighbourhood_summary["neighbourhood"] == neighbourhood]
            st.dataframe(filtered, use_container_width=True)
        else:
            st.dataframe(neighbourhood_summary, use_container_width=True)

        top_n = st.slider("Select number of neighbourhoods", min_value=5, max_value=22, value=10)

        if "total_estimated_revenue_proxy" in neighbourhood_summary.columns:
            st.subheader("Top Neighbourhoods by Estimated Revenue Proxy")
            top_revenue = (
                neighbourhood_summary
                .sort_values("total_estimated_revenue_proxy", ascending=False)
                .head(top_n)
                .set_index("neighbourhood")
            )
            st.bar_chart(top_revenue["total_estimated_revenue_proxy"])

        if "listing_count" in neighbourhood_summary.columns:
            st.subheader("Top Neighbourhoods by Listing Count")
            top_supply = (
                neighbourhood_summary
                .sort_values("listing_count", ascending=False)
                .head(top_n)
                .set_index("neighbourhood")
            )
            st.bar_chart(top_supply["listing_count"])

        if "median_price" in neighbourhood_summary.columns:
            st.subheader("Top Neighbourhoods by Median Price")
            top_price = (
                neighbourhood_summary
                .sort_values("median_price", ascending=False)
                .head(top_n)
                .set_index("neighbourhood")
            )
            st.bar_chart(top_price["median_price"])

        st.info(
            """
            Neighbourhood comparisons should be interpreted together with supply volume.
            A high median price in a small neighbourhood may not represent the whole market.
            """
        )


# ---------------------------------------------------------------------
# Page 4: Host & Review Insights
# ---------------------------------------------------------------------

elif page == "Host & Review Insights":
    st.header("Host & Review Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Host Portfolio Summary")

        if host_portfolio_summary.empty:
            show_missing_message("host_portfolio_summary_from_src.csv")
        else:
            st.dataframe(host_portfolio_summary, use_container_width=True)

            if "host_portfolio_segment" in host_portfolio_summary.columns:
                chart_data = host_portfolio_summary.set_index("host_portfolio_segment")
                st.bar_chart(chart_data["listing_count"])

    with col2:
        st.subheader("Review Score Summary")

        if review_score_summary.empty:
            show_missing_message("review_score_summary_from_src.csv")
        else:
            st.dataframe(review_score_summary, use_container_width=True)

            if "review_score_band" in review_score_summary.columns:
                chart_data = review_score_summary.set_index("review_score_band")
                st.bar_chart(chart_data["listing_count"])

    st.markdown(
        """
        **Business interpretation:**  
        Host portfolio size and review quality help explain market structure.
        Review scores are useful, but they are often concentrated near the high end,
        so they should be interpreted carefully.
        """
    )


# ---------------------------------------------------------------------
# Page 5: ML Price Prediction
# ---------------------------------------------------------------------

elif page == "ML Price Prediction":
    st.header("Machine Learning Price Prediction")

    st.markdown(
        """
        The project trains multiple regression models to estimate Airbnb listing price.
        The final selected model is the Random Forest Regressor.
        """
    )

    if ml_final_summary.empty:
        show_missing_message("ml_final_summary_from_src.csv")
    else:
        st.subheader("Final ML Summary")
        st.dataframe(ml_final_summary, use_container_width=True)

    if model_comparison.empty:
        show_missing_message("model_comparison_from_src.csv")
    else:
        st.subheader("Model Comparison")
        st.dataframe(model_comparison, use_container_width=True)

        if "model_name" in model_comparison.columns and "rmse" in model_comparison.columns:
            chart_data = model_comparison.set_index("model_name")
            st.subheader("RMSE by Model")
            st.bar_chart(chart_data["rmse"])

    if feature_importance.empty:
        show_missing_message("random_forest_feature_importance_from_src.csv")
    else:
        st.subheader("Top 15 Random Forest Feature Importances")
        top_features = feature_importance.head(15).set_index("feature")
        st.bar_chart(top_features["importance"])
        st.dataframe(feature_importance.head(20), use_container_width=True)

    if residual_summary.empty:
        show_missing_message("random_forest_residual_summary_from_src.csv")
    else:
        st.subheader("Residual Summary")
        st.dataframe(residual_summary, use_container_width=True)

    st.subheader("ML Diagnostic Figures")

    figure_paths = [
        ML_FIGURES_DIR / "actual_vs_predicted_price_random_forest_from_src.png",
        ML_FIGURES_DIR / "prediction_error_distribution_random_forest_from_src.png",
        ML_FIGURES_DIR / "random_forest_top_feature_importance_from_src.png",
    ]

    for figure_path in figure_paths:
        if figure_path.exists():
            st.image(str(figure_path), caption=figure_path.name, use_container_width=True)

    st.info(
        """
        The ML model is a decision-support model. It should not be treated as a perfect pricing engine.
        It performs better for common price ranges and struggles more with unusual or luxury listings.
        """
    )


# ---------------------------------------------------------------------
# Page 6: AI Innovation & Limitations
# ---------------------------------------------------------------------

elif page == "AI Innovation & Limitations":
    st.header("AI Innovation & Limitations")

    st.subheader("Open Innovation Concept")

    st.markdown(
        """
        A future extension of this project is an **AI-powered Airbnb Market Intelligence Assistant**.

        This assistant could help users ask natural language questions such as:

        - Which neighbourhoods have the highest estimated revenue proxy?
        - Which room types perform best?
        - Why is a listing predicted to be expensive?
        - Which features influence price prediction?
        - Where does the model struggle?
        - What are the risks of interpreting occupancy proxy?
        """
    )

    st.subheader("Responsible AI Guardrails")

    st.markdown(
        """
        The proposed AI assistant should follow these guardrails:

        - Do not treat estimated revenue proxy as actual revenue.
        - Do not treat occupancy proxy as confirmed occupancy.
        - Do not make unsupported claims about individual hosts or guests.
        - Always mention limitations when using proxy metrics.
        - Use warehouse outputs and reports instead of guessing.
        - Keep a human-in-the-loop for important decisions.
        """
    )

    st.subheader("Project Documentation")

    selected_doc = st.selectbox(
        "Select documentation file",
        [
            "ai_llm_usage_and_open_innovation.md",
            "model_card.md",
            "rubric_alignment.md",
            "warehouse_design.md",
        ],
    )

    doc_text = read_markdown_file(DOCS_DIR / selected_doc)
    st.markdown(doc_text)