import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from src.logger import logger
from src.exception import CustomException
class CryptoDataTransformer:
    """
    CryptoDataTransformer is a class designed to handle the transformation of cryptocurrency data by adding technical indicators 
    and saving the transformed data to a specified output file.

    Attributes:
        input_csv_path (str): The file path to the input CSV containing raw cryptocurrency data.
        output_csv_path (str): The file path to save the transformed data.

    Methods:
        __init__(input_csv_path, output_csv_path):
            Initializes the CryptoDataTransformer with input and output file paths.

        add_technical_indicators(df):
            Adds technical indicators such as SMA, EMA, RSI, and MACD to the given DataFrame.

            Args:
                df (pd.DataFrame): The input DataFrame containing raw cryptocurrency data.

            Returns:
                pd.DataFrame: The DataFrame with added technical indicators.

            Raises:
                CustomException: If an error occurs while adding technical indicators.

        transform_data():
            Transforms the raw cryptocurrency data by adding technical indicators, handling missing values, 
            and saving the transformed data to the output file.

            Returns:
                pd.DataFrame: The transformed DataFrame.

            Raises:
                CustomException: If an error occurs during the data transformation process.
    """
    def __init__(self, input_csv_path, output_csv_path):
        self.input_csv_path = input_csv_path
        self.output_csv_path = output_csv_path

    def add_technical_indicators(self, df):
        try:
            logger.info("Adding technical indicators to the data")

            # Simple Moving Average (SMA)
            df['sma_14'] = SMAIndicator(close=df['close'], window=14).sma_indicator()

            # Exponential Moving Average (EMA)
            df['ema_14'] = EMAIndicator(close=df['close'], window=14).ema_indicator()

            # Relative Strength Index (RSI)
            df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()

            # MACD (Moving Average Convergence Divergence)
            macd = MACD(close=df['close'])
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            df['macd_diff'] = macd.macd_diff()

            return df

        except Exception as e:
            logger.error("Error while adding technical indicators")
            raise CustomException(e, sys.exc_info())

    def transform_data(self):
        try:
            logger.info("Starting data transformation process")

            # Load raw data
            df = pd.read_csv(self.input_csv_path)
            logger.info(f"Raw data shape: {df.shape}")

            # Fill missing values forward for simplicity
            df.fillna(method='ffill', inplace=True) # type: ignore

            # Add indicators
            df = self.add_technical_indicators(df)

            # Drop any rows still containing NaNs (from indicator lag)
            df.dropna(inplace=True)
            logger.info(f"Transformed data shape: {df.shape}")

            # Save the transformed data
            os.makedirs(os.path.dirname(self.output_csv_path), exist_ok=True)
            df.to_csv(self.output_csv_path, index=False)
            logger.info(f"Transformed data saved to {self.output_csv_path}")

            return df

        except Exception as e:
            logger.error("Data transformation failed")
            raise CustomException(e, sys)

# Test run
if __name__ == "__main__":
    input_path = "data/BTC_USD_daily.csv"
    output_path = "data/BTC_USD_transformed.csv"
    transformer = CryptoDataTransformer(input_path, output_path)
    transformer.transform_data()
