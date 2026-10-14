import pandas as pd
import numpy as np
from pathlib import Path


# BIZINTEL AI - REALISTIC BUSINESS DATA GENERATOR

np.random.seed(42)

# SETTINGS


DAYS = 180
START_DATE = "2026-04-01"

output_folder = Path("dataset")
output_folder.mkdir(exist_ok=True)

dates = pd.date_range(
    start=START_DATE,
    periods=DAYS,
    freq="D"
)

# ---------------------------------------------------------
# 1. PRODUCTS
# ---------------------------------------------------------

products_data = [
    ("Rice 5kg", "Grocery", 420, 500, 1.2),
    ("Wheat Flour 5kg", "Grocery", 180, 220, 1.0),
    ("Sugar 1kg", "Grocery", 42, 50, 1.3),
    ("Cooking Oil 1L", "Grocery", 110, 135, 1.4),
    ("Tea Powder 250g", "Grocery", 95, 120, 1.0),
    ("Coffee 200g", "Grocery", 140, 180, 0.8),
    ("Biscuits Pack", "Grocery", 20, 28, 1.8),
    ("Noodles Pack", "Grocery", 35, 45, 1.5),
    ("Milk 1L", "Grocery", 48, 55, 2.0),
    ("Bread", "Grocery", 35, 45, 1.7),
    ("Eggs Pack", "Grocery", 60, 75, 1.8),

    ("Soap", "Personal Care", 30, 40, 1.3),
    ("Shampoo", "Personal Care", 110, 145, 0.8),
    ("Toothpaste", "Personal Care", 75, 95, 1.0),
    ("Toothbrush", "Personal Care", 35, 50, 0.7),
    ("Detergent 1kg", "Cleaning", 90, 120, 1.0),
    ("Dishwash", "Cleaning", 55, 70, 0.8),
    ("Handwash", "Personal Care", 80, 105, 0.9),
    ("Face Wash", "Personal Care", 120, 160, 0.6),
    ("Body Lotion", "Personal Care", 150, 200, 0.5),

    ("Notebook", "Stationery", 40, 55, 1.2),
    ("Pen Pack", "Stationery", 30, 45, 1.6),
    ("Pencil Pack", "Stationery", 20, 30, 1.3),
    ("Marker", "Stationery", 25, 40, 0.8),

    ("USB Cable", "Electronics", 120, 180, 0.7),
    ("Phone Charger", "Electronics", 300, 420, 0.5),
    ("Earphones", "Electronics", 250, 350, 0.6),
    ("Power Bank", "Electronics", 700, 900, 0.3),
    ("LED Bulb", "Electronics", 100, 140, 0.7),
    ("Extension Board", "Electronics", 250, 330, 0.4),

    ("Water Bottle", "Household", 120, 170, 0.8),
    ("Lunch Box", "Household", 180, 250, 0.5),

    ("T-Shirt", "Clothing", 300, 450, 0.5),
    ("Jeans", "Clothing", 700, 950, 0.3),
    ("Socks", "Clothing", 80, 120, 0.8),
    ("Cap", "Clothing", 120, 180, 0.5),

    ("Battery Pack", "Electronics", 100, 140, 0.7),
    ("Torch", "Electronics", 180, 250, 0.4),
    ("Umbrella", "Household", 200, 300, 0.4),
    ("Backpack", "Accessories", 500, 700, 0.4)
]

products = pd.DataFrame(
    products_data,
    columns=[
        "product_name",
        "category",
        "purchase_price",
        "selling_price",
        "demand_factor"
    ]
)

products.insert(
    0,
    "product_id",
    [f"P{i:03d}" for i in range(1, len(products) + 1)]
)

products["reorder_level"] = np.random.randint(
    10, 25, len(products)
)

products["initial_stock"] = np.random.randint(
    30, 80, len(products)
)

# ---------------------------------------------------------
# SAVE PRODUCT DATA
# ---------------------------------------------------------

products.to_csv(
    output_folder / "products.csv",
    index=False
)

# ---------------------------------------------------------
# 2. SALES + PURCHASES
# ---------------------------------------------------------

stock = dict(
    zip(
        products["product_id"],
        products["initial_stock"]
    )
)

sales_records = []
purchase_records = []

for date in dates:

    # -----------------------------------------------------
    # BUSINESS GROWTH
    # -----------------------------------------------------
    # Sales gradually increase over time.

    growth_factor = 1 + (dates.get_loc(date) / DAYS) * 0.20

    # -----------------------------------------------------
    # WEEKEND EFFECT
    # -----------------------------------------------------

    if date.weekday() >= 5:
        weekend_factor = 1.25
    else:
        weekend_factor = 1.0

    # -----------------------------------------------------
    # MONTHLY SEASONAL EFFECT
    # -----------------------------------------------------

    if date.month in [5, 6]:
        seasonal_factor = 1.10
    elif date.month in [7, 8]:
        seasonal_factor = 0.95
    else:
        seasonal_factor = 1.0

    # -----------------------------------------------------
    # PROCESS EACH PRODUCT
    # -----------------------------------------------------

    for _, product in products.iterrows():

        product_id = product["product_id"]

        # -------------------------------------------------
        # RESTOCK WHEN INVENTORY IS LOW
        # -------------------------------------------------

        if stock[product_id] <= product["reorder_level"]:

            # Bigger restock for popular products
            restock_quantity = int(
                40 + product["demand_factor"] * 35
            )

            purchase_records.append({
                "date": date,
                "product_id": product_id,
                "quantity": restock_quantity,
                "purchase_price": product["purchase_price"],
                "purchase_cost":
                    restock_quantity *
                    product["purchase_price"]
            })

            stock[product_id] += restock_quantity

        # -------------------------------------------------
        # EXPECTED DEMAND
        # -------------------------------------------------

        expected_demand = (
            product["demand_factor"]
            * 3
            * growth_factor
            * weekend_factor
            * seasonal_factor
        )

        # Add randomness
        quantity_demand = np.random.poisson(
            expected_demand
        )

        # Cannot sell more than available stock
        quantity_sold = min(
            quantity_demand,
            stock[product_id]
        )

        # -------------------------------------------------
        # RECORD SALE
        # -------------------------------------------------

        if quantity_sold > 0:

            revenue = (
                quantity_sold *
                product["selling_price"]
            )

            sales_records.append({
                "date": date,
                "product_id": product_id,
                "quantity": quantity_sold,
                "selling_price": product["selling_price"],
                "revenue": revenue
            })

            stock[product_id] -= quantity_sold


# ---------------------------------------------------------
# CREATE DATAFRAMES
# ---------------------------------------------------------

sales = pd.DataFrame(sales_records)

purchases = pd.DataFrame(
    purchase_records
)

# ---------------------------------------------------------
# 3. EXPENSES
# ---------------------------------------------------------

expense_records = []

for date in dates:

    if date.day == 1:

        # Small monthly variations
        expense_records.extend([
            {
                "date": date,
                "category": "Rent",
                "amount": round(
                    np.random.normal(12000, 300), 2
                )
            },
            {
                "date": date,
                "category": "Electricity",
                "amount": round(
                    np.random.normal(3500, 500), 2
                )
            },
            {
                "date": date,
                "category": "Internet",
                "amount": round(
                    np.random.normal(800, 50), 2
                )
            },
            {
                "date": date,
                "category": "Transport",
                "amount": round(
                    np.random.normal(2500, 400), 2
                )
            },
            {
                "date": date,
                "category": "Maintenance",
                "amount": round(
                    np.random.normal(1500, 500), 2
                )
            }
        ])

expenses = pd.DataFrame(
    expense_records
)

# ---------------------------------------------------------
# SAVE EVERYTHING
# ---------------------------------------------------------

sales.to_csv(
    output_folder / "sales.csv",
    index=False
)

purchases.to_csv(
    output_folder / "purchases.csv",
    index=False
)

expenses.to_csv(
    output_folder / "expenses.csv",
    index=False
)

# ---------------------------------------------------------
# FINAL REPORT
# ---------------------------------------------------------

print("=" * 50)
print("      BIZINTEL AI DATA GENERATOR")
print("=" * 50)

print("\nDataset generated successfully!")

print("\nFiles created:")
print("✓ products.csv")
print("✓ sales.csv")
print("✓ purchases.csv")
print("✓ expenses.csv")

print("\nDataset sizes:")
print(f"Products  : {len(products)}")
print(f"Sales     : {len(sales)}")
print(f"Purchases : {len(purchases)}")
print(f"Expenses  : {len(expenses)}")

print("\nDate range:")
print(f"{dates.min().date()} → {dates.max().date()}")

print("\nFinal inventory:")
print(f"{sum(stock.values())} units")

print("=" * 50)