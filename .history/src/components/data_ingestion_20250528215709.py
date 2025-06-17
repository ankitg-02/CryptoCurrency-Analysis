import os
import sys
import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logger
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

CRYPTOCOMPARE_API_KEY = "b23310723c937c5ec1b537592a3bfa80119d66f5e5dddc6b46290f55cf5e0ea2"

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join('artifacts', 'raw_data.csv')
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Starting Data Ingestion...")
        try:
            df = pd.read_csv('data/your_crypto_data.csv')  # Replace with actual path
            logging.info('Dataset loaded successfully.')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False)

            logging.info('Splitting data into train & test sets...')
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False)

            logging.info('Data ingestion completed successfully.')

            return self.ingestion_config.train_data_path, self.ingestion_config.test_data_path

        except Exception as e:
            logging.error('Error during data ingestion')
            raise CustomException(e, sys)

if __name__ == "__main__":
    ingestion = DataIngestion()
    train_path, test_path = ingestion.initiate_data_ingestion()

    transformation = DataTransformation()
    train_arr, test_arr = transformation.initiate_data_transformation(train_path, test_path)

    trainer = ModelTrainer()
    trainer.initiate_model_trainer(train_arr, test_arr)


