import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
from flask_cors import CORS
# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)  # 改為 INFO 級別
logging.getLogger('filelock').setLevel(logging.WARNING)  # 設置 filelock 的日誌級別為 WARNING
logging.getLogger('urllib3').setLevel(logging.WARNING)  # 設置 urllib3 的日誌級別為 WARNING

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
CORS(app)

# Configure cache
app.config['CACHE_TYPE'] = os.environ.get('CACHE_TYPE', 'SimpleCache')  # Use 'RedisCache' for production
app.config['CACHE_DEFAULT_TIMEOUT'] = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql://postgres:password@localhost:5432/house_rental")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

# Initialize cache
from cache import init_cache
init_cache(app)

# Import routes after app creation to avoid circular imports
from routes import *

from backend.routes.search import search_bp
app.register_blueprint(search_bp, url_prefix='/api/search')

from backend.routes.llm_api import llm_bp
app.register_blueprint(llm_bp, url_prefix='/api/llm')

if __name__ == "__main__":
    with app.app_context():
        # Import models to ensure tables are created
        import models
        # Note: We don't create tables here as they should be created via init.sql
        app.run(host="0.0.0.0", port=5000, debug=True)