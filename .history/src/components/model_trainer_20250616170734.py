import os
import sys
from dataclasses import dataclass
from catboost import CatBoostRegressor
from sklearn.metrics import r2_score
import numpy as np

from src.exception import CustomException
from src.utils import save_object, evaluate_models

@dataclass
class CryptoModelTrainer:
    def __init__(self):
        self.model_path = os.path.join('artifacts', 'model.pkl')

    def train_model(self, X_train, X_test, y_train, y_test):
        try:
            models = {
                "CatBoost": CatBoostRegressor(
                    verbose=False,
                    allow_writing_files=False
                )
            }

            # Ensure all data is numeric
            X_train = X_train.astype(float)
            X_test = X_test.astype(float)
            y_train = y_train.astype(float)
            y_test = y_test.astype(float)

            model_report = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models
            )

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            save_object(self.model_path, best_model)

            return best_model_score

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    trainer = CryptoModelTrainer()
    # Add test code here if needed

