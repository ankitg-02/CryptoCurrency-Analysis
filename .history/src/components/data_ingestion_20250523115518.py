import os
import sys
import requests
import pandas as pd
from src.logger import logger
from src.exception import CustomException

CRYPTOCOMPARE_API_KEY=b23310723c937c5ec1b537592a3bfa80119d66f5e5dddc6b46290f55cf5e0ea2

class CryptoDataIngestion:
    def __init__(self, symbol='BTC', currency='USD', limit=2000):
        self.api_key = CRYPTOCOMPARE_API_KEY
        self.symbol = symbol
        self.currency = currency
        self.limit = limit
        self.output_dir = "data"
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_data(self):
        try:
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
                raise CustomException(data.get('Message', 'Unknown error'), sys)

            df = pd.DataFrame(data['Data']['Data'])
            df['time'] = pd.to_datetime(df['time'], unit='s')
            output_path = os.path.join(self.output_dir, f"{self.symbol}_{self.currency}_daily.csv")
            df.to_csv(output_path, index=False)

            logger.info(f"Data saved to {output_path}")
            return output_path

        except Exception as e:
            raise CustomException(e, sys)
