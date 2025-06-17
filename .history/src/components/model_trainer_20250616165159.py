import os
import sys
from dataclasses import dataclass
import numpy as np
from catboost import CatBoostRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.logger import logger
from src.exception import CustomException
from src.utils import save_object, evaluate_models

@dataclass
class CryptoModelTrainer:
    def __init__(self):
        self.model_path = os.path.join('artifacts', 'model.pkl')

    def train_model(self, X_train, X_test, y_train, y_test):
        try:
            models = {
                "CatBoost Regressor": CatBoostRegressor(verbose=False)
            }

            # Train and evaluate models
            model_report = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models
            )

            # Get best model score
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            # Save the best model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            save_object(self.model_path, best_model)

            return best_model_score

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    trainer = CryptoModelTrainer()
    # Add test code here if needed

