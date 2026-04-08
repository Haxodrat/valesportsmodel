# backend/routes/rankings.py

from __future__ import annotations

from flask import Blueprint, jsonify

from services.rankings import load_region_rankings

rankings_bp = Blueprint("rankings_bp", __name__)


@rankings_bp.route("/rankings/<region>", methods=["GET"])
def get_rankings(region: str):
    try:
        payload = load_region_rankings(region=region, season=2026, mode="vct_only")
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500