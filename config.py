import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///crypto_users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True