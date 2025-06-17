import os
import sys
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.logger import logger
from src.exception import CustomException

@dataclass
class CryptoDataTransformer:
    def __init__(self, input_csv_path: str, output_csv_path: str):
        self.input_csv_path = input_csv_path
        self.output_csv_path = output_csv_path

    def transform_data(self):
        try:
            # Read the data
            df = pd.read_csv(self.input_csv_path)
            logger.info(f"Read data shape: {df.shape}")
            
            # Basic data validation
            if df.empty:
                raise ValueError("Input DataFrame is empty")
            
            # Convert time column to datetime
            df['time'] = pd.to_datetime(df['time'])
            
            # Feature engineering
            df['daily_return'] = df['close'].pct_change()
            df['volatility'] = df['daily_return'].rolling(window=30).std()
            df['MA_50'] = df['close'].rolling(window=50).mean()
            df['MA_200'] = df['close'].rolling(window=200).mean()
            
            # Drop NaN values
            df = df.dropna()
            logger.info(f"Shape after dropping NaN: {df.shape}")
            
            if df.empty:
                raise ValueError("DataFrame is empty after preprocessing")
            
            # Scale numeric features
            scaler = StandardScaler()
            numeric_features = ['open', 'high', 'low', 'close', 'volumefrom', 'volumeto']
            
            # Verify numeric features exist
            missing_features = [col for col in numeric_features if col not in df.columns]
            if missing_features:
                raise ValueError(f"Missing features: {missing_features}")
            
            df[numeric_features] = scaler.fit_transform(df[numeric_features])
            logger.info(f"Final transformed shape: {df.shape}")
            
            # Save transformed data
            os.makedirs(os.path.dirname(self.output_csv_path), exist_ok=True)
            df.to_csv(self.output_csv_path, index=False)
            logger.info(f"Transformed data saved to {self.output_csv_path}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error in data transformation: {str(e)}")
            raise CustomException(e, sys)

if __name__ == "__main__":
    # Example usage
    input_path = "path/to/your/input.csv"
    output_path = "path/to/your/output.csv"
    transformer = CryptoDataTransformer(input_path, output_path)
    transformer.transform_data()
