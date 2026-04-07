# An automated, serverless data pipeline

An automated, serverless data pipeline built with Python and Azure Functions. This application fetches historical and daily market data alongside macroeconomic indicators, storing the raw datasets in Azure Blob Storage. It serves as the foundational data ingestion layer for downstream quantitative analysis and agentic AI trading models.

## 🚀 Features

* **Serverless Architecture:** Deployed as an Azure Function App with a Timer Trigger, running automatically every day at 21:00 UTC.
* **Market Data Ingestion:** Pulls 10-year historical daily interval data for major sector ETFs (SPY, XLK, XLU, XLF, XLV, XLE, XLY) using the `yfinance` library.
* **Macroeconomic Data:** Integrates with the St. Louis Fed (FRED) API to track inflation via the Consumer Price Index (CPI).
* **Cloud Storage:** Automatically processes and uploads the datasets (as `.csv` and `.json` files) directly into an Azure Blob Storage container (`raw-market-data`).
* **CI/CD Pipeline:** Fully automated deployment to Azure using GitHub Actions.

## 🛠️ Tech Stack

* **Language:** Python 3.12
* **Compute:** Azure Functions (v2 Programming Model)
* **Storage:** Azure Blob Storage
* **CI/CD:** GitHub Actions
* **Key Libraries:** `yfinance`, `pandas`, `requests`, `azure-storage-blob`, `azure-functions`

## ⚙️ Environment Variables

To run this function locally or deploy it to your own Azure environment, you need to configure the following environment variables in your `local.settings.json` or Azure App Configuration:

| Variable Name | Description |
| :--- | :--- |
| `AZURE_CONNECTION_STRING` | Your Azure Storage account connection string for Blob Storage. |
| `FRED_API_KEY` | API key from the Federal Reserve Economic Data (FRED). |

*(Note: The function is designed to skip macro data fetching gracefully and log a warning if the `FRED_API_KEY` is not provided).*

## 📂 Project Structure

* `function_app.py`: The core application logic containing the Timer Trigger, API calls, and Azure Blob upload functions.
* `host.json`: Azure Functions configuration and logging settings.
* `requirements.txt`: Python package dependencies.
* `.github/workflows/main_trading-bot-v3.yml`: The GitHub Actions workflow for building and deploying the package to Azure.

## 🔄 CI/CD & Deployment

This repository uses GitHub Actions for continuous integration and deployment. Upon pushing to the `main` branch, the workflow:
1. Sets up the Python 3.12 environment.
2. Installs the dependencies from `requirements.txt` into a local target folder.
3. Packages the application.
4. Authenticates with Azure via OIDC (using GitHub Secrets).
5. Deploys the package to the `trading-bot-v3` Azure Function App in the Production slot.

## 👤 Author
**MSM Macksood**
