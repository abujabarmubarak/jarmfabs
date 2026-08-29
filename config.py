import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jarmfabs-technologies-secret-key-2026-super-secure'
    
    # Database: Use PostgreSQL if configured, otherwise fallback to SQLite
    # Format: postgresql://username:password@localhost:5432/jarmfabs_db
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url or f"sqlite:///{os.path.join(basedir, 'jarmfabs.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload directories (local disk storage)
    UPLOAD_FOLDER_GALLERY = os.path.join(basedir, 'static', 'uploads', 'gallery')
    UPLOAD_FOLDER_CLIENTS = os.path.join(basedir, 'static', 'uploads', 'clients')
    
    # Cloudinary support (optional, for persistent image hosting on free serverless)
    CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
