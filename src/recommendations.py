import pandas as pd

# Load datasets
products = pd.read_csv("D:/507/BIZIntel_AI/dataset/products.csv")
sales = pd.read_csv("D:/507/BIZIntel_AI/dataset/sales.csv")
purchases = pd.read_csv("D:/507/BIZIntel_AI/dataset/purchases.csv")

# Calculate current stock
purchased = purchases.groupby("product_id")["quantity"].sum()
sold = sales.groupby("product_id")["quantity"].sum()

products["purchased"] = (
    products["product_id"].map(purchased).fillna(0)
)
products["sold"] = (
    products["product_id"].map(sold).fillna(0)
)

products["current_stock"] = (
    products["initial_stock"]
    + products["purchased"]
    - products["sold"]
)

# Identify products at or below reorder level
low_stock = products[
    products["current_stock"] <= products["reorder_level"]
].copy()

print("\n========== RESTOCKING RECOMMENDATIONS ==========")

if low_stock.empty:
    print("No products currently require restocking.")
else:
    low_stock["suggested_order"] = (
        low_stock["reorder_level"] * 2
        - low_stock["current_stock"]
    ).clip(lower=0)

    print(
        low_stock[
            [
                "product_name",
                "current_stock",
                "reorder_level",
                "suggested_order"
            ]
        ].to_string(index=False)
    )
