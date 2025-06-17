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
    # Changed from train() to train_model()
    best_model = trainer.train_model(
        X_train=transformed_data.drop(['time', 'close'], axis=1),
        X_test=transformed_data.drop(['time', 'close'], axis=1),
        y_train=transformed_data['close'],
        y_test=transformed_data['close']
    )
    logger.info(f"Best model score: {best_model}")
    
except Exception as e:
    raise CustomException(e, sys)
