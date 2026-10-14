
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load sales
sales = pd.read_csv("D:/507/BIZIntel_AI/dataset/sales.csv")
sales["date"] = pd.to_datetime(sales["date"])

# Create complete daily demand series per product
all_dates = pd.date_range(
    sales["date"].min(),
    sales["date"].max(),
    freq="D"
)

products = pd.read_csv("D:/507/BIZIntel_AI/dataset/products.csv")
forecasts = []

for _, product in products.iterrows():
    pid = product["product_id"]

    daily = (
        sales[sales["product_id"] == pid]
        .groupby("date")["quantity"]
        .sum()
        .reindex(all_dates, fill_value=0)
        .rename("demand")
        .to_frame()
    )

    # Features: recent demand and calendar patterns
    daily["lag_1"] = daily["demand"].shift(1)
    daily["lag_7"] = daily["demand"].shift(7)
    daily["day_of_week"] = daily.index.dayofweek
    daily["day_of_month"] = daily.index.day

    data = daily.dropna()

    if len(data) < 30:
        continue

    features = [
        "lag_1", "lag_7",
        "day_of_week", "day_of_month"
    ]

    # Time-based holdout: last 14 days
    train = data.iloc[:-14]
    test = data.iloc[-14:]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(train[features], train["demand"])
    predictions = model.predict(test[features])

    mae = mean_absolute_error(
        test["demand"], predictions
    )

    # Refit using all historical data
    model.fit(data[features], data["demand"])

    # Recursive 7-day forecast
    history = daily["demand"].tolist()
    future_dates = pd.date_range(
        all_dates[-1] + pd.Timedelta(days=1),
        periods=7,
        freq="D"
    )

    for date in future_dates:
        row = pd.DataFrame([{
            "lag_1": history[-1],
            "lag_7": history[-7],
            "day_of_week": date.dayofweek,
            "day_of_month": date.day
        }])

        predicted = max(
            0, int(round(model.predict(row[features])[0]))
        )

        forecasts.append({
            "product_name": product["product_name"],
            "forecast_date": date.date(),
            "predicted_demand": predicted,
            "test_mae": round(mae, 2)
        })

        history.append(predicted)

# Save forecasts
result = pd.DataFrame(forecasts)
result.to_csv("D:/507/BIZIntel_AI/dataset/forecasts.csv", index=False)

print("\n7-DAY DEMAND FORECAST")
print(
    result.groupby("product_name")["predicted_demand"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nAverage holdout MAE:",
      round(result["test_mae"].mean(), 2))

print("\nSaved forecasts to dataset/forecasts.csv")
