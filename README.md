project-root/
│
├── app/
│   └── main.py                   # FastAPI or Flask app
│
├── data/                         # CSV or processed data
├── notebooks/                    # Jupyter notebooks for EDA
│
├── src/
│   ├── components/               # ML logic split in modules
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   └── __init__.py
│   │
│   ├── pipeline/                 # High-level training/prediction flow
│   │   ├── train_pipeline.py
│   │   ├── predict_pipeline.py
│   │   └── __init__.py
│   │
│   ├── exception.py              # Custom exception class
│   ├── logger.py                 # Logging setup
│   └── utils.py                  # Helper functions
│
├── Dockerfile
├── docker-compose.yml
└── README.md
