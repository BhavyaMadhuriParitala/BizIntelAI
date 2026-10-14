import pandas as pd

# =========================================================
# LOAD DATA
# =========================================================

sales = pd.read_csv("D:/507/BIZIntel_AI/dataset/sales.csv")
purchases = pd.read_csv("D:/507/BIZIntel_AI/dataset/purchases.csv")
expenses = pd.read_csv("D:/507/BIZIntel_AI/dataset/expenses.csv")
products = pd.read_csv("D:/507/BIZIntel_AI/dataset/products.csv")


# =========================================================
# TOTAL REVENUE
# =========================================================

total_revenue = sales["revenue"].sum()


# =========================================================
# COST OF GOODS SOLD
# =========================================================

# Merge sales with product purchase prices
sales_with_cost = sales.merge(
    products[["product_id", "purchase_price"]],
    on="product_id",
    how="left"
)

# Cost of products actually sold
sales_with_cost["cost"] = (
    sales_with_cost["quantity"]
    * sales_with_cost["purchase_price"]
)

total_cogs = sales_with_cost["cost"].sum()


# =========================================================
# GROSS PROFIT
# =========================================================

gross_profit = total_revenue - total_cogs


# =========================================================
# OPERATING EXPENSES
# =========================================================

total_expenses = expenses["amount"].sum()


# =========================================================
# NET PROFIT
# =========================================================

net_profit = gross_profit - total_expenses


# =========================================================
# PROFIT MARGIN
# =========================================================

profit_margin = (
    net_profit / total_revenue
) * 100


# =========================================================
# INVENTORY
# =========================================================

# Total units purchased
purchased_units = (
    purchases
    .groupby("product_id")["quantity"]
    .sum()
)

# Total units sold
sold_units = (
    sales
    .groupby("product_id")["quantity"]
    .sum()
)

# Combine purchase and sales information
inventory = products[
    [
        "product_id",
        "product_name",
        "category",
        "purchase_price",
        "reorder_level",
        "initial_stock"
    ]
].copy()

inventory["purchased"] = (
    inventory["product_id"]
    .map(purchased_units)
    .fillna(0)
)

inventory["sold"] = (
    inventory["product_id"]
    .map(sold_units)
    .fillna(0)
)

inventory["current_stock"] = (
    inventory["initial_stock"]
    + inventory["purchased"]
    - inventory["sold"]
)

inventory["inventory_value"] = (
    inventory["current_stock"]
    * inventory["purchase_price"]
)


# =========================================================
# BUSINESS REPORT
# =========================================================

print("=" * 55)
print("          BIZINTEL AI - BUSINESS REPORT")
print("=" * 55)

print(f"\nRevenue             : ₹{total_revenue:,.2f}")
print(f"COGS                : ₹{total_cogs:,.2f}")
print(f"Gross Profit        : ₹{gross_profit:,.2f}")
print(f"Operating Expenses  : ₹{total_expenses:,.2f}")
print(f"Net Profit          : ₹{net_profit:,.2f}")
print(f"Profit Margin       : {profit_margin:.2f}%")

print("\n" + "=" * 55)
print("INVENTORY")
print("=" * 55)

print(
    f"Total Inventory Value : "
    f"₹{inventory['inventory_value'].sum():,.2f}"
)

print(
    f"Total Units in Stock : "
    f"{inventory['current_stock'].sum():,.0f}"
)

print("\n" + "=" * 55)


# =========================================================
# PRODUCT-LEVEL INTELLIGENCE
# =========================================================

# Calculate sales and revenue for each product
product_sales = sales.groupby("product_id").agg(
    units_sold=("quantity", "sum"),
    revenue=("revenue", "sum")
).reset_index()

# Add product information
product_sales = product_sales.merge(
    products,
    on="product_id",
    how="left"
)

# Calculate product costs and profit
product_sales["cost"] = (
    product_sales["units_sold"]
    * product_sales["purchase_price"]
)

product_sales["profit"] = (
    product_sales["revenue"]
    - product_sales["cost"]
)

product_sales["profit_margin"] = (
    product_sales["profit"]
    / product_sales["revenue"].replace(0, float("nan"))
) * 100

# Rank products by revenue
top_products = product_sales.sort_values(
    "revenue", ascending=False
)

# Identify slow-moving products
slow_products = product_sales.sort_values(
    "units_sold", ascending=True
)

print("\n" + "=" * 55)
print("           PRODUCT INTELLIGENCE")
print("=" * 55)

print("\nTOP 5 PRODUCTS BY REVENUE")
print(
    top_products[
        ["product_name", "units_sold", "revenue", "profit"]
    ].head(5).to_string(index=False)
)

print("\n5 SLOWEST-SELLING PRODUCTS")
print(
    slow_products[
        ["product_name", "units_sold", "revenue", "profit"]
    ].head(5).to_string(index=False)
)


# =========================================================
# EXPENSE ANALYSIS
# =========================================================

expense_summary = (
    expenses.groupby("category")["amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "=" * 45)
print("          EXPENSE ANALYSIS")
print("=" * 45)

print(expense_summary.to_string())

# Visualize expenses
import matplotlib.pyplot as plt

expense_summary.plot(kind="bar")

plt.title("Operating Expenses by Category")
plt.xlabel("Expense Category")
plt.ylabel("Total Expense (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
