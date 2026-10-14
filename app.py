
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(
    page_title="BizIntel AI",
    page_icon="📊",
    layout="wide"
)

# Load datasets
DATA = Path(__file__).parent / "dataset"

@st.cache_data
def load_data():
    products = pd.read_csv(DATA / "products.csv")
    sales = pd.read_csv(DATA / "sales.csv", parse_dates=["date"])
    purchases = pd.read_csv(DATA / "purchases.csv")
    expenses = pd.read_csv(DATA / "expenses.csv")
    forecasts = pd.read_csv(DATA / "forecasts.csv")
    return products, sales, purchases, expenses, forecasts

products, sales, purchases, expenses, forecasts = load_data()

# Financial calculations
revenue = sales["revenue"].sum()

sales_cost = sales.merge(
    products[["product_id", "purchase_price"]],
    on="product_id",
    how="left"
)
cogs = (
    sales_cost["quantity"] * sales_cost["purchase_price"]
).sum()

total_expenses = expenses["amount"].sum()
gross_profit = revenue - cogs
net_profit = gross_profit - total_expenses
margin = net_profit / revenue * 100 if revenue else 0

# Inventory calculations
purchased = purchases.groupby("product_id")["quantity"].sum()
sold = sales.groupby("product_id")["quantity"].sum()

inventory = products.copy()
inventory["purchased"] = (
    inventory["product_id"].map(purchased).fillna(0)
)
inventory["sold"] = (
    inventory["product_id"].map(sold).fillna(0)
)
inventory["current_stock"] = (
    inventory["initial_stock"]
    + inventory["purchased"]
    - inventory["sold"]
)
inventory["inventory_value"] = (
    inventory["current_stock"] * inventory["purchase_price"]
)

# Product analytics
product_sales = sales.groupby("product_id").agg(
    units_sold=("quantity", "sum"),
    revenue=("revenue", "sum")
).reset_index()

product_sales = product_sales.merge(
    products[["product_id", "product_name", "purchase_price"]],
    on="product_id",
    how="left"
)
product_sales["profit"] = (
    product_sales["revenue"]
    - product_sales["units_sold"] * product_sales["purchase_price"]
)

# Header
st.title("📊 BizIntel AI")
st.caption("Small-business financial intelligence and demand forecasting")

st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Choose a section",
    ["Overview", "Products", "Sales Trends", "Inventory",
     "Demand Forecast", "Expenses"]
)

if page == "Overview":
    st.subheader("Business Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenue", f"₹{revenue:,.0f}")
    c2.metric("Gross Profit", f"₹{gross_profit:,.0f}")
    c3.metric("Net Profit", f"₹{net_profit:,.0f}")
    c4.metric("Net Margin", f"{margin:.2f}%")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Daily Revenue")
        daily = sales.groupby("date")["revenue"].sum()
        st.line_chart(daily)

    with c2:
        st.subheader("Top Products by Revenue")
        top = product_sales.nlargest(10, "revenue")
        st.bar_chart(top.set_index("product_name")["revenue"])

    st.subheader("Business Insights")
    best = product_sales.loc[product_sales["profit"].idxmax()]
    st.write(
        f"• **Most profitable product:** {best['product_name']} "
        f"(estimated product profit ₹{best['profit']:,.0f})."
    )
    st.write(f"• **Operating expenses:** ₹{total_expenses:,.0f}.")
    st.write(
        f"• **Inventory value:** ₹{inventory['inventory_value'].sum():,.0f}."
    )

    low = inventory[
        inventory["current_stock"] <= inventory["reorder_level"]
    ]
    st.write(f"• **Products at or below reorder level:** {len(low)}.")

elif page == "Products":
    st.subheader("Product Intelligence")

    ranking = st.selectbox(
        "Rank products by",
        ["Revenue", "Units Sold", "Profit"]
    )
    column = {
        "Revenue": "revenue",
        "Units Sold": "units_sold",
        "Profit": "profit"
    }[ranking]

    st.dataframe(
        product_sales.sort_values(column, ascending=False),
        use_container_width=True,
        hide_index=True
    )

elif page == "Sales Trends":
    st.subheader("Sales Trend Analysis")
    daily = sales.groupby("date")["revenue"].sum()
    st.line_chart(daily)
    st.subheader("Top 10 Sales Days")
    st.dataframe(
        daily.nlargest(10).rename("revenue").reset_index(),
        use_container_width=True,
        hide_index=True
    )

elif page == "Inventory":
    st.subheader("Inventory Management")

    low = inventory[
        inventory["current_stock"] <= inventory["reorder_level"]
    ].copy()
    low["suggested_order"] = (
        2 * low["reorder_level"] - low["current_stock"]
    ).clip(lower=0)

    st.metric("Total Units in Stock", int(inventory["current_stock"].sum()))
    st.metric("Inventory Value", f"₹{inventory['inventory_value'].sum():,.0f}")

    st.write("Products requiring restocking")
    st.dataframe(
        low[["product_name", "current_stock", "reorder_level",
             "suggested_order"]],
        use_container_width=True,
        hide_index=True
    )
    st.write("Full inventory")
    st.dataframe(inventory, use_container_width=True, hide_index=True)

elif page == "Demand Forecast":
    st.subheader("ML-Based 7-Day Demand Forecast")
    st.caption(
        "Predictions from the trained Random Forest model. "
        "These are estimates, not guaranteed future sales."
    )

    summary = forecasts.groupby("product_name").agg(
        predicted_7_day_demand=("predicted_demand", "sum"),
        holdout_MAE=("test_mae", "first")
    ).reset_index()

    st.dataframe(
        summary.sort_values("predicted_7_day_demand", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    selected = st.selectbox(
        "Inspect a product",
        summary["product_name"].tolist()
    )
    detail = forecasts[forecasts["product_name"] == selected].copy()
    detail["forecast_date"] = pd.to_datetime(detail["forecast_date"])
    st.bar_chart(
        detail.set_index("forecast_date")["predicted_demand"]
    )

elif page == "Expenses":
    st.subheader("Operating Expense Analysis")
    expense_summary = (
        expenses.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(expense_summary)
    st.dataframe(
        expense_summary.rename("amount").reset_index(),
        use_container_width=True,
        hide_index=True
    )

st.divider()
st.caption(
    "BizIntel AI | Analytics + Machine Learning + "
    "Rule-Based Decision Support"
)
