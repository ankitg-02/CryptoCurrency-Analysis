import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.components.data_ingestion import CryptoDataIngestion
from src.components.data_transformation import CryptoDataTransformer
from src.components.model_trainer import CryptoModelTrainer

if __name__ == "__main__":
    raw_path = CryptoDataIngestion().fetch_data()
    transformed_path = "data/BTC_USD_transformed.csv"
    CryptoDataTransformer(raw_path, transformed_path).transform_data()
    CryptoModelTrainer(transformed_path, "models/random_forest_model.pkl").train()
