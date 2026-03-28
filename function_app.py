import azure.functions as func
import logging
import traceback

app = func.FunctionApp()

try:
    # --- HEAVY IMPORTS ---
    import os
    import json
    import tempfile
    import yfinance as yf
    import requests
    import pandas as pd
    from datetime import datetime
    from azure.storage.blob import BlobServiceClient

    # --- REAL APP LOGIC ---
    FRED_API_KEY = os.getenv("FRED_API_KEY")
    AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
    CONTAINER_NAME = "raw-market-data"

    def upload_to_azure(file_path, file_name):
        logging.info(f"Uploading {file_name} to Azure...")
        try:
            blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
            blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_name)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            logging.info(f"Successfully uploaded {file_name} to Azure.")
        except Exception as e:
            logging.error(f"Azure Upload Failed: {e}")

    def fetch_market_data():
        logging.info("Fetching ETF data...")
        tickers = ["XLK", "XLU", "SPY"]
        data = yf.download(tickers, period="1y", interval="1d")
        filename = f"market_data_{datetime.now().strftime('%Y%m%d')}.csv"
        filepath = os.path.join(tempfile.gettempdir(), filename)
        data.to_csv(filepath)
        upload_to_azure(filepath, filename)
        os.remove(filepath)

    def fetch_macro_data():
        logging.info("Fetching Macro data...")
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&api_key={FRED_API_KEY}&file_type=json"
        response = requests.get(url)
        if response.status_code == 200:
            macro_data = response.json()
            filename = f"macro_data_{datetime.now().strftime('%Y%m%d')}.json"
            filepath = os.path.join(tempfile.gettempdir(), filename)
            with open(filepath, 'w') as f:
                json.dump(macro_data, f)
            upload_to_azure(filepath, filename)
            os.remove(filepath)
        else:
            logging.error(f"Failed to fetch macro data. Status Code: {response.status_code}")

    # --- REAL TRIGGER ---
    @app.timer_trigger(schedule="0 0 21 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
    def daily_market_fetch(myTimer: func.TimerRequest) -> None:
        logging.info('Automated trigger started: Fetching market and macro data.')
        if not AZURE_CONNECTION_STRING:
            logging.error("AZURE_CONNECTION_STRING is missing.")
            return
        fetch_market_data()
        if FRED_API_KEY:
            fetch_macro_data()
        else:
            logging.warning("Skipping FRED Macro Data: API key not configured.")
        logging.info('Automated trigger completed successfully.')

except Exception as e:
    # --- DIAGNOSTIC TRIGGER (Runs only if an import crashes) ---
    error_msg = traceback.format_exc()
    
    @app.timer_trigger(schedule="0 0 21 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
    def daily_market_fetch(myTimer: func.TimerRequest) -> None:
        logging.error("=== FATAL MODULE IMPORT ERROR ===")
        logging.error(error_msg)
