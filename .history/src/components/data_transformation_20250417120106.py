import os
import sys
import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator

from src.exception import CustomException
from src.logger import logger

class CryptoDataTransformer:
    def __init__(self, input_csv_path, output_csv_path):
        self.input_csv_path = input_csv_path
        self.output_csv_path = output_csv_path

    def add_technical_indicators(self, df):
        try:
            logger.info("Adding technical indicators to the data")

            # Simple Moving Average (SMA)
            df['sma_14'] = SMAIndicator(close=df['close'], window=14).sma_indicator()

            # Exponential Moving Average (EMA)
            df['ema_14'] = EMAIndicator(close=df['close'], window=14).ema_indicator()

            # Relative Strength Index (RSI)
            df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()

            # MACD (Moving Average Convergence Divergence)
            macd = MACD(close=df['close'])
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            df['macd_diff'] = macd.macd_diff()

            return df

        except Exception as e:
            logger.error("Error while adding technical indicators")
            raise CustomException(e, sys)

    def transform_data(self):
        try:
            logger.info("Starting data transformation process")

            # Load raw data
            df = pd.read_csv(self.input_csv_path)
            logger.info(f"Raw data shape: {df.shape}")

            # Fill missing values forward for simplicity
            df.fillna(method='ffill', inplace=True)

            # Add indicators
            df = self.add_technical_indicators(df)

            # Drop any rows still containing NaNs (from indicator lag)
            df.dropna(inplace=True)
            logger.info(f"Transformed data shape: {df.shape}")

            # Save the transformed data
            os.makedirs(os.path.dirname(self.output_csv_path), exist_ok=True)
            df.to_csv(self.output_csv_path, index=False)
            logger.info(f"Transformed data saved to {self.output_csv_path}")

            return df

        except Exception as e:
            logger.error("Data transformation failed")
            raise CustomException(e, sys)

# Test run
if __name__ == "__main__":
    input_path = "data/BTC_USD_daily.csv"
    output_path = "data/BTC_USD_transformed.csv"
    transformer = CryptoDataTransformer(input_path, output_path)
    transformer.transform_data()
