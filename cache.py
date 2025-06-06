
import os
from flask_caching import Cache

# Initialize cache instance
cache = Cache()

def init_cache(app):
    """Initialize cache with the Flask app"""
    # Configure cache based on environment
    redis_url = os.environ.get('REDIS_URL')
    
    if redis_url:
        # Production: Use Redis
        app.config['CACHE_TYPE'] = 'RedisCache'
        app.config['CACHE_REDIS_URL'] = redis_url
    else:
        # Development: Use SimpleCache
        app.config['CACHE_TYPE'] = 'SimpleCache'
    
    app.config['CACHE_DEFAULT_TIMEOUT'] = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
    
    # Initialize cache with app
    cache.init_app(app)
    
    return cache
