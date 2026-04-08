# backend/api.py

from flask import Blueprint

from routes.matches import matches_bp


api_bp = Blueprint("api_bp", __name__)
api_bp.register_blueprint(matches_bp)