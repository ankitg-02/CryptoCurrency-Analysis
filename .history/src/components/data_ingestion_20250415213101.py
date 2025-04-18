import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("CRYPTOCOMPARE_API_KEY")

def fetch_crypto_data(symbol='BTC', currency='USD', limit=2000):
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        'fsym': symbol,      # From symbol
        'tsym': currency,    # To symbol
        'limit': limit,      # Number of days
        'api_key': API_KEY
    }

    res = requests.get(url, params=params)
    data = res.json()

    if data['Response'] != 'Success':
        raise Exception("Error fetching data")

    df = pd.DataFrame(data['Data']['Data'])
    df['time'] = pd.to_datetime(df['time'], unit='s')  # Convert UNIX timestamp
    df.to_csv(f'data/{symbol}_{currency}_daily.csv', index=False)
    print(f"Data saved to data/{symbol}_{currency}_daily.csv")
    return df

if __name__ == "__main__":
    fetch_crypto_data('BTC', 'USD')
