# run_ingestion.py (place this in the root directory)

from src.components.data_ingestion import CryptoDataIngestion

if __name__ == "__main__":
    ingestion = CryptoDataIngestion(symbol='BTC', currency='USD', limit=2000)
    ingestion.fetch_data()
