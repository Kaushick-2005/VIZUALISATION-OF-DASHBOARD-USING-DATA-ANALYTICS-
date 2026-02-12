import pandas as pd
import numpy as np
from datetime import datetime


def load_data(path: str = "data/superstore.csv") -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    # try parsing date columns
    for col in ["Order Date", "Ship Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return clean_data(df)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # numeric conversions
    if "Sales" in df.columns:
        df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce").fillna(0.0)
    if "Profit" in df.columns:
        df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce").fillna(0.0)
    if "Quantity" in df.columns:
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)

    # strip whitespace for group keys
    string_keys = [c for c in ["Region", "State", "City", "Category", "Sub-Category", "Segment", "Customer ID"] if c in df.columns]
    for c in string_keys:
        df[c] = df[c].astype(str).str.strip()

    return df


def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "Order Date" not in df.columns:
        raise ValueError("Order Date column missing")
    df["YearMonth"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    ms = df.groupby("YearMonth")["Sales"].sum().reset_index()
    return ms


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    if "Region" not in df.columns:
        return pd.DataFrame(columns=["Region", "Sales"]).astype(object)
    return df.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)


def top_n_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if "Product ID" in df.columns and "Product Name" in df.columns:
        return (
            df.groupby(["Product ID", "Product Name"], as_index=False)["Sales"]
            .sum()
            .sort_values("Sales", ascending=False)
            .head(n)
        )
    return pd.DataFrame()


def compute_rfm(df: pd.DataFrame, ref_date: datetime = None) -> pd.DataFrame:
    if ref_date is None:
        if "Order Date" in df.columns:
            ref_date = df["Order Date"].max() + pd.Timedelta(days=1)
        else:
            ref_date = pd.Timestamp.today()

    agg = df.groupby("Customer ID").agg(
        recency_days=("Order Date", lambda x: (ref_date - x.max()).days if not x.isna().all() else np.nan),
        frequency=("Order ID", "nunique"),
        monetary=("Sales", "sum"),
    ).reset_index()

    # avoid qcut errors on identical values
    for col in ["recency_days", "frequency", "monetary"]:
        if agg[col].nunique() < 5:
            agg[col + "_rank"] = agg[col].rank(method="first")
        else:
            agg[col + "_rank"] = agg[col]

    # create RFM scores 1-5
    try:
        agg["R_score"] = pd.qcut(agg["recency_days"].rank(method="first", ascending=False), 5, labels=[1, 2, 3, 4, 5]).astype(int)
        agg["F_score"] = pd.qcut(agg["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
        agg["M_score"] = pd.qcut(agg["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    except Exception:
        # fallback: use ranks
        agg["R_score"] = pd.cut(agg["recency_days"].rank(method="first", ascending=False), bins=5, labels=[1, 2, 3, 4, 5]).astype(int)
        agg["F_score"] = pd.cut(agg["frequency"].rank(method="first"), bins=5, labels=[1, 2, 3, 4, 5]).astype(int)
        agg["M_score"] = pd.cut(agg["monetary"].rank(method="first"), bins=5, labels=[1, 2, 3, 4, 5]).astype(int)

    agg["RFM_Score"] = agg["R_score"].astype(str) + agg["F_score"].astype(str) + agg["M_score"].astype(str)
    return agg


# US state name -> abbreviation mapping used for choropleth
US_STATE_ABBREV = {
    'Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR','California': 'CA','Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE','District of Columbia': 'DC','Florida': 'FL','Georgia': 'GA','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO','Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY','North Carolina': 'NC','North Dakota': 'ND','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virginia': 'VA','Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'
}


def add_state_abbrev(df: pd.DataFrame, state_col: str = "State") -> pd.DataFrame:
    df = df.copy()
    if state_col in df.columns:
        df["state_abbrev"] = df[state_col].map(US_STATE_ABBREV).fillna("")
    else:
        df["state_abbrev"] = ""
    return df
