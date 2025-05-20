import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import pandas as pd
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator

from src.logger import logger
from src.exception import CustomException

class CryptoDataTransformer:
    def __init__(self, input_csv_path, output_csv_path):
        self.input_csv_path = input_csv_path
        self.output_csv_path = output_csv_path

    def add_technical_indicators(self, df):
        try:
            df['sma_14'] = SMAIndicator(close=df['close'], window=14).sma_indicator()
            df['ema_14'] = EMAIndicator(close=df['close'], window=14).ema_indicator()
            df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()

            macd = MACD(close=df['close'])
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            df['macd_diff'] = macd.macd_diff()

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def transform_data(self):
        try:
            df = pd.read_csv(self.input_csv_path)
            df.fillna(method='ffill', inplace=True)
            df = self.add_technical_indicators(df)
            df.dropna(inplace=True)
            os.makedirs(os.path.dirname(self.output_csv_path), exist_ok=True)
            df.to_csv(self.output_csv_path, index=False)
            logger.info(f"Transformed data saved at {self.output_csv_path}")
            return df

        except Exception as e:
            raise CustomException(e, sys)
