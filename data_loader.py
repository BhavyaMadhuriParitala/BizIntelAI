"""

src/
│
├── data_loader.py       ← load & inspect data
├── analytics.py         ← calculate business metrics
├── visualization.py     ← graphs
├── forecasting.py       ← ML
└── recommendations.py   ← intelligent recommendations
"""

import pandas as pd

sales = pd.read_csv("D:/507/BIZIntel_AI/dataset/sales.csv")

print(sales.head())
print("\nShape:", sales.shape)
print("\nColumns:")
print(sales.columns)