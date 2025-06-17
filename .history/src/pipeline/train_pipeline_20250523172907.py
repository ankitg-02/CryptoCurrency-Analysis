import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.components.data_ingestion import CryptoDataIngestion
from src.components.data_transformation import CryptoDataTransformer
from src.components.model_trainer import CryptoModelTrainer
from src.logger import logger
from src.exception import CustomException

if __name__ == "__main__":
    try:
        # Ingestion
        ingestion = CryptoDataIngestion(symbol="BTC", currency="USD", limit=2000)
        raw_csv_path = ingestion.fetch_data()

        # Transformation
        transformed_csv_path = "data/BTC_USD_daily_transformed.csv"
        transformer = CryptoDataTransformer(input_csv_path=raw_csv_path, output_csv_path=transformed_csv_path)
        transformer.transform_data()

        # Training
        model_path = "models/random_forest_model.pkl"
        trainer = CryptoModelTrainer(csv_path=transformed_csv_path, model_path=model_path)
        trainer.train()

    except Exception as e:
        raise CustomException(e, sys)
