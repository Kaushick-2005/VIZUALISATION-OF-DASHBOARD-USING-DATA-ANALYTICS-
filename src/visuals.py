import plotly.express as px
import pandas as pd
from typing import Optional


def plot_region_bar(df: pd.DataFrame, title: str = "Region-wise Sales"):
    if "Region" not in df.columns:
        return None
    region_sales = df.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig = px.bar(region_sales, x="Region", y="Sales", color="Region", title=title)
    return fig


def plot_category_pie(df: pd.DataFrame, title: str = "Sales by Category"):
    if "Category" not in df.columns:
        return None
    cat = df.groupby("Category", as_index=False)["Sales"].sum()
    fig = px.pie(cat, names="Category", values="Sales", title=title)
    return fig


def plot_monthly_trend(ms_df: pd.DataFrame, date_col: str = "YearMonth", value_col: str = "Sales", title: str = "Monthly Sales Trend"):
    if ms_df is None or ms_df.empty:
        return None
    fig = px.line(ms_df, x=date_col, y=value_col, title=title)
    return fig


def plot_rfm_scatter(rfm_df: pd.DataFrame, title: str = "RFM: Monetary vs Frequency"):
    if rfm_df is None or rfm_df.empty:
        return None
    fig = px.scatter(rfm_df, x="frequency", y="monetary", color="RFM_Score", hover_data=["Customer ID", "recency_days"], title=title, size_max=12)
    return fig


def plot_state_choropleth(df: pd.DataFrame, state_col: str = "state_abbrev", value_col: str = "Sales", title: str = "Sales by State"):
    if state_col not in df.columns:
        return None
    agg = df.groupby(state_col, as_index=False)[value_col].sum()
    # remove blank abbrevs
    agg = agg[agg[state_col].astype(bool)]
    if agg.empty:
        return None
    fig = px.choropleth(agg, locations=state_col, locationmode="USA-states", color=value_col, scope="usa", title=title)
    return fig
