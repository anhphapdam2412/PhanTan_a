import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecretkey')

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///library/WebStore.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False