from flask import Flask
from flask_session import Session
import logging

app = Flask(__name__)

# Session configuration
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

from app import routes