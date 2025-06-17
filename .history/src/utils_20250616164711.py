import os
import sys
import pickle
import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logger


def save_object(file_path, obj):
    """
    Save a Python object to a file using pickle.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)

        logging.info(f"Object saved successfully at {file_path}")

    except Exception as e:
        logging.error("Failed to save object", exc_info=True)
        raise CustomError(e, sys)


def load_object(file_path):
    """
    Load a pickled Python object from a file.
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        logging.error("Failed to load object", exc_info=True)
        raise CustomError(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, param_grid):
    """
    Perform hyperparameter tuning using GridSearchCV and evaluate models.
    Returns a dictionary of model names and their R2 scores on test data.
    """
    try:
        report = {}

        for model_name, model in models.items():
            logging.info(f"Training model: {model_name}")
            params = param_grid.get(model_name, {})

            if params:
                grid_search = GridSearchCV(model, param_grid=params, cv=3, scoring='r2', verbose=0, n_jobs=-1)
                grid_search.fit(X_train, y_train)
                best_model = grid_search.best_estimator_
            else:
                model.fit(X_train, y_train)
                best_model = model

            y_pred = best_model.predict(X_test)
            score = r2_score(y_test, y_pred)
            report[model_name] = score

            logging.info(f"{model_name} R2 score: {score:.4f}")

        return report

    except Exception as e:
        logging.error("Model evaluation failed", exc_info=True)
        raise CustomError(e, sys)
