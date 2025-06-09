from flask import Blueprint
from .listings import listings_bp
from .search import search_bp
from .llm_api import llm_bp


def init_app(app):
    app.register_blueprint(search_bp, url_prefix='/api/smart-search')
    app.register_blueprint(llm_bp, url_prefix='/api/llm')
    app.register_blueprint(listings_bp ,url_prefix='/api/listings')
