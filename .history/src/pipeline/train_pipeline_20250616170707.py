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
    
    # Prepare features for training
    numeric_features = ['open', 'high', 'low', 'volumefrom', 'volumeto', 
                       'daily_return', 'volatility', 'MA_20', 'MA_50']
    
    X = transformed_data[numeric_features]
    y = transformed_data['close']
    
    # Model Training
    trainer = CryptoModelTrainer()
    best_model = trainer.train_model(
        X_train=X,
        X_test=X,  # Using same data for demonstration
        y_train=y,
        y_test=y   # Using same data for demonstration
    )
    logger.info(f"Best model score: {best_model}")
    
except Exception as e:
    logger.error(f"Error in training pipeline: {str(e)}")
    raise CustomException(e, sys)
