import sys
import os
import numpy as np
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.logger import logger
from src.exception import CustomException

class CryptoDataTransformer:
    def __init__(self, input_csv_path, output_csv_path):
        self.input_csv_path = input_csv_path
        self.output_csv_path = output_csv_path

    def SMA(self, series, window):
        return series.rolling(window=window).mean()

    def EMA(self, series, window):
        return series.ewm(span=window, adjust=False).mean()

    def RSI(self, series, window=14):
        delta = series.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)

        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def MACD(self, series, fast=12, slow=26, signal=9):
        ema_fast = self.EMA(series, fast)
        ema_slow = self.EMA(series, slow)
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        macd_diff = macd_line - signal_line
        return macd_line, signal_line, macd_diff

    def add_technical_indicators(self, df):
        try:
            df['sma_14'] = self.SMA(df['close'], 14)
            df['ema_14'] = self.EMA(df['close'], 14)
            df['rsi'] = self.RSI(df['close'], 14)

            macd_line, signal_line, macd_diff = self.MACD(df['close'])
            df['macd'] = macd_line
            df['macd_signal'] = signal_line
            df['macd_diff'] = macd_diff

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
