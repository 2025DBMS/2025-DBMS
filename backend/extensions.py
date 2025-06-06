from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

# Initialize extensions
db = SQLAlchemy()
cache = Cache() 