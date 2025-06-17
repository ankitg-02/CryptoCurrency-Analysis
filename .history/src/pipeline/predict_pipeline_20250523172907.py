import os
import sys
import pickle
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.logger import logger
from src.exception import CustomException

def predict_new_data(model_path: str, data_path: str):
    try:
        # Load model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # Load data
        df = pd.read_csv(data_path)
        X = df.drop(columns=['close', 'time'])

        # Predict
        predictions = model.predict(X)

        # Display result
        df['predicted_close'] = predictions
        print(df[['time', 'close', 'predicted_close']].tail(10))
        return df

    except Exception as e:
        raise CustomException(e, sys)

if __name__ == "__main__":
    model_path = "models/random_forest_model.pkl"
    data_path = "data/BTC_USD_daily_transformed.csv"
    predict_new_data(model_path, data_path)
