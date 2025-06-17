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
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join('artifacts', 'best_model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logger.info("Starting model training...")

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1], train_array[:, -1], test_array[:, :-1], test_array[:, -1]
            )

            models = {
                'RandomForestRegressor': RandomForestRegressor(),
                'DecisionTreeRegressor': DecisionTreeRegressor(),
                'GradientBoostingRegressor': GradientBoostingRegressor(),
                'LinearRegression': LinearRegression(),
                'KNeighborsRegressor': KNeighborsRegressor(),
                'CatBoostRegressor': CatBoostRegressor(verbose=0),
                'XGBRegressor': XGBRegressor(),
                'AdaBoostRegressor': AdaBoostRegressor()
            }

            param_grid = {
                'RandomForestRegressor': {'n_estimators': [100, 200], 'max_depth': [10, 20]},
                'DecisionTreeRegressor': {'max_depth': [10, 20]},
                'GradientBoostingRegressor': {'n_estimators': [100, 200], 'learning_rate': [0.1, 0.2]},
                'LinearRegression': {},
                'KNeighborsRegressor': {'n_neighbors': [3, 5]},
                'CatBoostRegressor': {'iterations': [500], 'depth': [6]},
                'XGBRegressor': {'n_estimators': [100], 'learning_rate': [0.1]},
                'AdaBoostRegressor': {'n_estimators': [100], 'learning_rate': [0.1]}
            }

            logger.info("Hyperparameter tuning started...")
            model_report = evaluate_models(X_train, y_train, X_test, y_test, models, param_grid)

            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]

            logger.info(f"Best model selected: {best_model_name} with R²: {model_report[best_model_name]:.4f}")

            best_model.fit(X_train, y_train)

            save_object(self.model_trainer_config.trained_model_file_path, best_model)

            y_pred = best_model.predict(X_test)
            r2 = r2_score(y_test, y_pred)

            logger.info(f"Best model trained and saved. Final R² score: {r2:.4f}")
            print(f"🏆 Best Model: {best_model_name} | Final R² Score: {r2:.4f}")

            return r2

        except Exception as e:
            logger.error("Error during model training", exc_info=True)
            raise CustomException(e, sys)

