import os
import sys
import pandas as pd

from src.exception import CustomException
from src.logger import logger

class CryptoDataTransformer:
    def __init__(self, input_csv_path, output_csv_path):
        self.input_csv_path = os.path.abspath(input_csv_path)
        self.output_csv_path = os.path.abspath(output_csv_path)

    # Placeholder if you want to add simple manual indicators without ta package
    def add_basic_indicators(self, df):
        try:
            # Example: simple moving average 14 days
            df['sma_14'] = df['close'].rolling(window=14).mean()
            # Example: exponential moving average 14 days
            df['ema_14'] = df['close'].ewm(span=14, adjust=False).mean()
            # Example: simple RSI calculation can be added manually if needed

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def transform_data(self):
        try:
            if not os.path.exists(self.input_csv_path):
                raise CustomException(f"Input file not found: {self.input_csv_path}", sys)

            df = pd.read_csv(self.input_csv_path)
            df.fillna(method='ffill', inplace=True)
            df = self.add_basic_indicators(df)
            df.dropna(inplace=True)

            os.makedirs(os.path.dirname(self.output_csv_path), exist_ok=True)
            df.to_csv(self.output_csv_path, index=False)

            logger.info(f"Transformed data saved at {self.output_csv_path}")
            return df

        except Exception as e:
            raise CustomException(e, sys)
