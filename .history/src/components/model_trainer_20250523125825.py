import os
import sys
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

from src.logger import logger
from src.exception import CustomException

class CryptoModelTrainer:
    def __init__(self, csv_path, model_path):
        self.csv_path = os.path.abspath(csv_path)
        self.model_path = os.path.abspath(model_path)

    def train(self):
        try:
            if not os.path.exists(self.csv_path):
                raise CustomException(f"Training data CSV not found: {self.csv_path}", sys)

            df = pd.read_csv(self.csv_path)
            
            # Make sure required columns are present
            if 'close' not in df.columns or 'time' not in df.columns:
                raise CustomException("Required columns 'close' and 'time' not found in CSV", sys)

            X = df.drop(columns=['close', 'time'])
            y = df['close']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = RandomForestRegressor(random_state=42)
            model.fit(X_train, y_train)

            predictions = model.predict(X_test)
            mse = mean_squared_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)

            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            with open(self.model_path, 'wb') as f:
                pickle.dump(model, f)

            logger.info(f"Model saved to {self.model_path} | MSE: {mse:.4f}, R2: {r2:.4f}")

        except Exception as e:
            raise CustomException(e, sys)
