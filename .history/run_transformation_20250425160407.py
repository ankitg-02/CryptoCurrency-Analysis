from src.components.data_transformation import CryptoDataTransformer

if __name__ == "__main__":
    transformer = CryptoDataTransformer(
        input_csv_path="data/BTC_USD_daily.csv",
        output_csv_path="data/BTC_USD_transformed.csv"
    )
    transformer.transform_data()
