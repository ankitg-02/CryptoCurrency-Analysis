import os
import sys
from src.components.data_ingestion import CryptoDataIngestion
from src.components.data_transformation import CryptoDataTransformer
from src.components.model_trainer import CryptoModelTrainer
from src.exception import CustomException
from src.logger import logger

try:
    # Data Ingestion
    ingestion = CryptoDataIngestion()
    raw_csv_path = ingestion.fetch_data()
    
    # Data Transformation
    transformed_csv_path = os.path.join('artifacts', 'transformed_data.csv')
    transformer = CryptoDataTransformer(
        input_csv_path=raw_csv_path,
        output_csv_path=transformed_csv_path
    )
    transformed_data = transformer.transform_data()
    
    # Model Training
    trainer = CryptoModelTrainer()
    # Add model training code here
    
except Exception as e:
    raise CustomException(e, sys)
