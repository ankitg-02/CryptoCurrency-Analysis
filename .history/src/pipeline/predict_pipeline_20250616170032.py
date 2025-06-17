import os
import sys
import pandas as pd
import numpy as np
import pickle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.exception import CustomException
from src.logger import logger

def predict_new_data(model_path='artifacts/model.pkl', data_path='artifacts/transformed_data.csv'):
    try:
        # Verify paths exist
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file not found at: {data_path}")
            
        # Load the model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            
        # Load and prepare data
        df = pd.read_csv(data_path)
        
        # Make predictions
        predictions = model.predict(df)
        
        # Save predictions
        output_path = os.path.join('artifacts', 'predictions.csv')
        pd.DataFrame(predictions, columns=['predictions']).to_csv(output_path, index=False)
        logger.info(f"Predictions saved to {output_path}")
        
        return predictions
        
    except Exception as e:
        logger.error(f"Error in prediction pipeline: {str(e)}")
        raise CustomException(e, sys)

if __name__ == "__main__":
    # Use the model path from training pipeline
    model_path = os.path.join('artifacts', 'model.pkl')
    data_path = os.path.join('artifacts', 'transformed_data.csv')
    predict_new_data(model_path, data_path)
