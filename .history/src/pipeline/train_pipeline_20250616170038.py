import os
import sys
from src.components.data_ingestion import CryptoDataIngestion
from src.components.data_transformation import CryptoDataTransformer
from src.components.model_trainer import CryptoModelTrainer
from src.exception import CustomException
from src.logger import logger
from src.utils import save_object

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
    best_model = trainer.train(transformed_data)
    
    # Save the best model
    model_path = os.path.join('artifacts', 'model.pkl')
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    save_object(model_path, best_model)
    logger.info(f"Model saved to {model_path}")
    
except Exception as e:
    raise CustomException(e, sys)
