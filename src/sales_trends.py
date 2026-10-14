
import pandas as pd
import matplotlib.pyplot as plt

# Load sales data
sales = pd.read_csv("D:/507/BIZIntel_AI/dataset/sales.csv")

# Convert date column
sales["date"] = pd.to_datetime(sales["date"])

# Calculate daily revenue
daily_sales = (
    sales.groupby("date")["revenue"]
    .sum()
    .reset_index()
)

# Display the highest-revenue days
print("\nTOP 5 SALES DAYS")
print(
    daily_sales.sort_values("revenue", ascending=False)
    .head(5)
    .to_string(index=False)
)

# Plot daily sales trend
plt.figure(figsize=(12, 12))
plt.plot(
    daily_sales["date"],
    daily_sales["revenue"]
)

plt.title("Daily Sales Revenue Trend")
plt.xlabel("Date")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
