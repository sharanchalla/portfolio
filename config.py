import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-key')
    
    # Resolve relative SQLite URL to be absolute relative to this project's root folder
    db_url = os.environ.get('DATABASE_URL', 'sqlite:///database/portfolio.db')
    if db_url.startswith('sqlite:///'):
        db_path = db_url.replace('sqlite:///', '')
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, db_path).replace('\\', '/')
    else:
        SQLALCHEMY_DATABASE_URI = db_url
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
