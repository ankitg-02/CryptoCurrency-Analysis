import os
import sys
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.logger import logger
from src.exception import CustomException

@dataclass
class CryptoDataTransformer:
    def __init__(self):
        pass

    def transform_data(self, data_path):
        try:
            # Read the data
            df = pd.read_csv(data_path)
            
            # Convert time column to datetime
            df['time'] = pd.to_datetime(df['time'])
            
            # Feature engineering
            df['daily_return'] = df['close'].pct_change()
            df['volatility'] = df['daily_return'].rolling(window=30).std()
            df['MA_50'] = df['close'].rolling(window=50).mean()
            df['MA_200'] = df['close'].rolling(window=200).mean()
            
            # Drop NaN values
            df = df.dropna()
            
            # Scale numeric features
            scaler = StandardScaler()
            numeric_features = ['open', 'high', 'low', 'close', 'volumefrom', 'volumeto']
            df[numeric_features] = scaler.fit_transform(df[numeric_features])
            
            return df
            
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    transformer = CryptoDataTransformer()
    # Add test code here if needed
