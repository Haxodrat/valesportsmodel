# backend/routes/matches.py

from __future__ import annotations

from flask import Blueprint, jsonify

from services.predictions import get_upcoming_predictions

matches_bp = Blueprint("matches_bp", __name__)


@matches_bp.route("/upcoming-matches", methods=["GET"])
def upcoming_matches():
    try:
        matches = get_upcoming_predictions(season=2026, mode="vct_only")
        return jsonify({"data": matches}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500