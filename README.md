# Real-Time Crypto Price ETL Pipeline with Google Cloud Functions & BigQuery

## Overview
This project is a **serverless ETL pipeline** that fetches **real-time cryptocurrency prices** from the **CoinGecko API** and loads the data into **Google BigQuery**. The pipeline is deployed using **Google Cloud Functions**, allowing scheduled or on-demand execution.

## Features
- Fetches **Bitcoin (BTC), Ethereum (ETH), and Tether (USDT)** prices in **USD and THB**.
- Uses **Google Cloud Functions** for serverless execution.
- Loads data into **Google BigQuery** for real-time analytics.
- Uses **pandas** for data transformation.
- Stores timestamps in **Yangon Time (Asia/Yangon timezone).**
- Designed for easy integration with **Power BI DirectQuery** for real-time reporting.

## Technologies Used
- **Python** (requests, pandas, datetime, pytz)
- **Google Cloud Functions** (Serverless execution)
- **Google BigQuery** (Data storage and analytics)
- **CoinGecko API** (Real-time cryptocurrency prices)

## Setup Instructions
### 1. Google Cloud Setup
- Enable **Google Cloud Functions** and **BigQuery API** in your Google Cloud project.
- Create a **BigQuery dataset** and table with the following schema:

  ```sql
  CREATE TABLE `crypto-price-live-dashboard.crypto_prices.crypto_prices_data` (
      timestamp TIMESTAMP,
      bitcoin_usd FLOAT,
      bitcoin_thb FLOAT,
      ethereum_usd FLOAT,
      ethereum_thb FLOAT,
      tether_usd FLOAT,
      tether_thb FLOAT
  );
  ```

### 2. Deploy Cloud Function
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/crypto-etl.git
   cd crypto-etl
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Deploy to Google Cloud Functions:
   ```sh
   gcloud functions deploy fetch_and_insert_crypto \
       --runtime python39 \
       --trigger-http \
       --allow-unauthenticated
   ```

## Code Explanation
- **fetch_and_insert_crypto(request):** Entry point for Cloud Function.
- **insert_data_into_bigquery(data):** Loads data into BigQuery.
- **Yangon timezone handling:** Ensures timestamps are stored in **Asia/Yangon** timezone.
- **Error Handling:** Catches and logs errors during API requests and BigQuery inserts.

## Example Data Entry
| timestamp            | bitcoin_usd | bitcoin_thb | ethereum_usd | ethereum_thb | tether_usd | tether_thb |
|----------------------|------------|------------|--------------|--------------|------------|------------|
| 2024-03-10 12:00:00 | 65000.0    | 2300000.0  | 3500.0       | 123000.0     | 1.00       | 35.00      |

## Usage
- Schedule the Cloud Function using **Cloud Scheduler** for automatic execution.
- Connect BigQuery to **Power BI** using **DirectQuery** for live crypto price analysis.

## License
This project is open-source and available under the MIT License.
