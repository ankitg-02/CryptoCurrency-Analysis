import os
import sys
import pandas as pd
from src.logger import logger
from src.exception import CustomException

class CryptoDataTransformer:
    def __init__(self, input_csv_path):
        self.input_csv_path = input_csv_path
        self.output_csv_path = os.path.join("artifacts", "data", "processed", "transformed_data.csv")

    def transform_data(self):
        try:
            df = pd.read_csv(self.input_csv_path)
            df.fillna(method='ffill', inplace=True)
            df.dropna(inplace=True)
            os.makedirs(os.path.dirname(self.output_csv_path), exist_ok=True)
            df.to_csv(self.output_csv_path, index=False)
            logger.info(f"Transformed data saved at {self.output_csv_path}")
            return self.output_csv_path

        except Exception as e:
            raise CustomException(e, sys)