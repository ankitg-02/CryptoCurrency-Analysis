import os
import sys
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from dataclasses import dataclass

from src.logger import logger
from src.exception import CustomException
#from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_path: str = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            num_columns = ['open', 'high', 'low', 'volumefrom', 'volumeto']

            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])

            logger.info("Numerical pipeline created successfully.")

            preprocessor = ColumnTransformer(transformers=[
                ('num_pipeline', num_pipeline, num_columns)
            ])

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logger.info("Train and test data loaded for transformation.")

            target_column = 'close'

            X_train = train_df.drop(columns=[target_column, 'time'], errors='ignore')
            y_train = train_df[target_column]

            X_test = test_df.drop(columns=[target_column, 'time'], errors='ignore')
            y_test = test_df[target_column]

            preprocessor = self.get_data_transformer_object()

            X_train_transformed = preprocessor.fit_transform(X_train)
            X_test_transformed = preprocessor.transform(X_test)

            train_array = np.c_[X_train_transformed, y_train]
            test_array = np.c_[X_test_transformed, y_test]

            save_object(self.transformation_config.preprocessor_path, preprocessor)

            logger.info("Data transformation complete. Preprocessor saved.")

            return train_array, test_array

        except Exception as e:
            raise CustomException(e, sys)
