BizIntel AI 📊

AI-Powered Business Intelligence for Small Retail Businesses

BizIntel AI is a Python-based business intelligence dashboard designed to help small retail businesses understand their financial performance, analyze product sales, monitor inventory, and make data-driven decisions.

The project combines data analytics, rule-based recommendations, and machine learning to turn retail data into actionable business insights.

## Features

- **Financial Analytics:** Track revenue, cost of goods sold (COGS), gross profit, operating expenses, net profit, and profit margin.
- **Product Intelligence:** Identify top-performing and slow-selling products.
- **Sales Trend Analysis:** Explore daily sales patterns and revenue trends.
- **Inventory Monitoring:** Review available stock and identify products that may require restocking.
- **Restocking Recommendations:** Generate inventory suggestions using rule-based logic.
- **Demand Forecasting:** Forecast short-term product demand using a Random Forest regression model.
- **Expense Analysis:** Examine operating expenses by category.
- **Interactive Dashboard:** Explore insights through a Streamlit web interface.

## 🛠️ Technology Stack

| Python | Core application logic |
| Streamlit | Interactive dashboard |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning and demand forecasting |
| Matplotlib | Data visualization |

## 📁 Project Structure

BIZIntel_AI/
├── main.py
├── app.py
├── generate_data.py
├── data_loader.py
├── requirements.txt
├── README.md
├── .gitignore
├── dataset/
│   ├── products.csv
│   ├── sales.csv
│   ├── purchases.csv
│   ├── expenses.csv
│   └── forecasts.csv
└── src/
    ├── analytics.py
    ├── forecasting.py
    ├── recommendations.py
    └── sales_trends.py

## Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/BhavyaMadhuriParitala/BizIntelAI.git
cd BizIntelAI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

If `main.py` is the file containing your Streamlit dashboard:

```bash
python -m streamlit run main.py
```

If your dashboard entry point is `app.py`, use:

```bash
python -m streamlit run app.py
```

Use the entry point that matches your actual project.

## Machine Learning

BizIntel AI uses a Random Forest regression model to forecast short-term product demand based on historical sales patterns and lag-based features.

The forecasts are intended to support inventory planning and purchasing decisions. Model performance should be evaluated on held-out data and validated using real retail data before relying on predictions for operational decisions.

## Data Disclaimer

The current prototype uses synthetic retail data for demonstration and development. Reported financial metrics, inventory insights, and forecasts are illustrative and are not verified results from real businesses.

## Target Users

- Independent grocery stores
- Convenience stores
- Small retail businesses
- Shop owners seeking clearer sales, expense, and inventory insights

## Future Improvements

- Import data from real point-of-sale and inventory systems.
- Improve forecast evaluation and compare alternative models.
- Enhance inventory planning and reporting.
- Deploy the application to a public cloud platform.
- Validate usability and business impact with real retailers.

## Project Status

BizIntel AI is an ongoing prototype demonstrating retail business analytics, rule-based inventory recommendations, and machine-learning-based demand forecasting.

## 👩‍💻 Author

**Bhavya Madhuri Paritala*

*Built with Python, data analytics, and machine learning.*
