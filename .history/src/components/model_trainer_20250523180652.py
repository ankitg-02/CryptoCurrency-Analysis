import os
import sys
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.logger import logger
from src.exception import CustomException

class CryptoModelTrainer:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.model_path = os.path.join("artifacts", "models", "crypto_model.pkl")

    def train(self):
        try:
            df = pd.read_csv(self.csv_path)
            X = df.drop(columns=['close', 'time'])
            y = df['close']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

            model = RandomForestRegressor()
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