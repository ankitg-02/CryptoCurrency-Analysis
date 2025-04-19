import os
import sys

# Add the project root directory to Python's module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import requests
import pandas as pd
from dotenv import load_dotenv

from src.logger import logger
from src.exception import CustomException

load_dotenv()

class CryptoDataIngestion:
    def __init__(self, symbol='BTC', currency='USD', limit=2000):
        self.api_key = os.getenv("CRYPTOCOMPARE_API_KEY")
        self.symbol = symbol
        self.currency = currency
        self.limit = limit
        self.output_dir = "data"
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_data(self):
        try:
            logger.info(f"Starting data ingestion for {self.symbol}/{self.currency}")

            url = "https://min-api.cryptocompare.com/data/v2/histoday"
            params = {
                'fsym': self.symbol,
                'tsym': self.currency,
                'limit': self.limit,
                'api_key': self.api_key
            }

            response = requests.get(url, params=params)
            data = response.json()

            if data['Response'] != 'Success':
                raise CustomException(f"API Error: {data.get('Message', 'Unknown error')}", sys)

            df = pd.DataFrame(data['Data']['Data'])
            df['time'] = pd.to_datetime(df['time'], unit='s')

            output_path = os.path.join(self.output_dir, f"{self.symbol}_{self.currency}_daily.csv")
            df.to_csv(output_path, index=False)

            logger.info(f"Data successfully saved to {output_path}")
            return df

        except Exception as e:
            logger.error("Error in data ingestion stage")
            raise CustomException(e, sys)

# For standalone testing
if __name__ == "__main__":
    ingestion = CryptoDataIngestion(symbol='BTC', currency='USD', limit=2000)
    ingestion.fetch_data()
