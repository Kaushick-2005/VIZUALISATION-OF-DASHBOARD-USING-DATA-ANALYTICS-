import streamlit as st
from src.data_processing import load_data, monthly_sales, sales_by_region, compute_rfm, add_state_abbrev, top_n_products
from src.visuals import plot_region_bar, plot_category_pie, plot_monthly_trend, plot_rfm_scatter, plot_state_choropleth


# Page configuration
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")


@st.cache_data
def get_data():
    return load_data("data/superstore.csv")


df = get_data()

st.title("📊 Visual Analytics Dashboard for Region-Wise Sales and Customer Insights")

# Sidebar global filters
st.sidebar.header("Global Filters")
regions = sorted(df["Region"].dropna().unique().tolist()) if "Region" in df.columns else []
categories = sorted(df["Category"].dropna().unique().tolist()) if "Category" in df.columns else []

sel_region = st.sidebar.multiselect("Region", options=regions, default=regions)
sel_category = st.sidebar.multiselect("Category", options=categories, default=categories)

filtered = df.copy()
if sel_region:
    filtered = filtered[filtered["Region"].isin(sel_region)]
if sel_category:
    filtered = filtered[filtered["Category"].isin(sel_category)]

# Pages
page = st.sidebar.radio("Page", ["Overview", "Region Insights", "Customer Insights", "Product Insights"]) 

if page == "Overview":
    st.header("Overview")
    total_sales = filtered["Sales"].sum()
    total_profit = filtered["Profit"].sum()
    total_orders = filtered["Order ID"].nunique() if "Order ID" in filtered.columns else 0
    total_customers = filtered["Customer ID"].nunique() if "Customer ID" in filtered.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Total Sales", f"${total_sales:,.0f}")
    c2.metric("📈 Total Profit", f"${total_profit:,.0f}")
    c3.metric("🧾 Orders", total_orders)
    c4.metric("👥 Customers", total_customers)

    st.markdown("---")
    # charts
    fig1 = plot_region_bar(filtered, title="Region Sales")
    fig2 = plot_category_pie(filtered, title="Category Share")
    ms = monthly_sales(filtered)
    fig3 = plot_monthly_trend(ms)

    colA, colB = st.columns([2, 1])
    with colA:
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)
    with colB:
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)

elif page == "Region Insights":
    st.header("Region & State Insights")
    st.write("Sales aggregated by region and US state (choropleth)")
    df_states = add_state_abbrev(filtered)
    fig_map = plot_state_choropleth(df_states, state_col="state_abbrev", value_col="Sales")
    if fig_map:
        st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("---")
    fig_reg = plot_region_bar(filtered, title="Region Sales (detailed)")
    if fig_reg:
        st.plotly_chart(fig_reg, use_container_width=True)

elif page == "Customer Insights":
    st.header("Customer RFM & Segmentation")
    st.write("Recency, Frequency, Monetary analysis for customers (RFM)")
    rfm = compute_rfm(filtered)
    st.dataframe(rfm.sort_values("monetary", ascending=False).head(20))
    fig_rfm = plot_rfm_scatter(rfm)
    if fig_rfm:
        st.plotly_chart(fig_rfm, use_container_width=True)

elif page == "Product Insights":
    st.header("Top Products")
    top_products = top_n_products(filtered, n=20)
    st.dataframe(top_products)
    st.markdown("---")
    st.write("Download filtered data:")
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "filtered_data.csv", "text/csv")

st.sidebar.markdown("---")
st.sidebar.write("Data rows: ", len(filtered))

st.success("Dashboard ready")
