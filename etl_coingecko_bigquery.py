import functions_framework
import requests
from google.cloud import bigquery
from datetime import datetime
import pytz
import pandas as pd

# Define Yangon timezone
yangon_tz = pytz.timezone("Asia/Yangon")

# Set up BigQuery client
client = bigquery.Client()

# Set your dataset and table
dataset_id = 'crypto-price-live-dashboard.crypto_prices.crypto_prices'  # Replace with your project ID and dataset name
table_id = 'crypto-price-live-dashboard.crypto_prices.crypto_prices_data'  # Replace with your table name

# API URL
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether&vs_currencies=usd,thb"

# Define schema for BigQuery table (adjust according to your BigQuery schema)
schema = [
    bigquery.SchemaField("timestamp", "TIMESTAMP"),
    bigquery.SchemaField("bitcoin_usd", "FLOAT"),
    bigquery.SchemaField("bitcoin_thb", "FLOAT"),
    bigquery.SchemaField("ethereum_usd", "FLOAT"),
    bigquery.SchemaField("ethereum_thb", "FLOAT"),
    bigquery.SchemaField("tether_usd", "FLOAT"),
    bigquery.SchemaField("tether_thb", "FLOAT")
]

# Function to insert data into BigQuery
def insert_data_into_bigquery(data):
    try:
        df = pd.DataFrame([data])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        job = client.load_table_from_dataframe(df, table_id)  # Batch insert
        job.result()  # Wait for the job to complete
        print(f"Data inserted at {data['timestamp']} (Yangon Time)")
        print(f"Data inserted at {data['timestamp']} (Yangon Time)")
    except Exception as e:
        print(f"Error inserting data: {e}")

# Cloud Function entry point
@functions_framework.http
def fetch_and_insert_crypto(request):
    # Get current time in Yangon timezone
    now = datetime.now(yangon_tz)
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Fetch cryptocurrency data
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Extract crypto prices
        bitcoin_usd = data['bitcoin']['usd']
        bitcoin_thb = data['bitcoin']['thb']
        ethereum_usd = data['ethereum']['usd']
        ethereum_thb = data['ethereum']['thb']
        tether_usd = data['tether']['usd']
        tether_thb = data['tether']['thb']

        # Prepare the data to insert into BigQuery
        data_to_insert = {
            'timestamp': timestamp,
            'bitcoin_usd': bitcoin_usd,
            'bitcoin_thb': bitcoin_thb,
            'ethereum_usd': ethereum_usd,
            'ethereum_thb': ethereum_thb,
            'tether_usd': tether_usd,
            'tether_thb': tether_thb
        }

        # Insert into BigQuery
        insert_data_into_bigquery(data_to_insert)

        return "Data inserted successfully", 200
    else:
        return "Error fetching data", 500