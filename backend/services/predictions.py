# backend/services/predictions.py

from __future__ import annotations

from data_sources.vlr_client import VLRClient
from ratings.elo import EloModel, EloConfig

import time

_ELO_CACHE = {"model": None, "built_at": 0}
CACHE_TTL_SECONDS = 300


def build_elo_model() -> EloModel:
    """
    Build the elo model based on historical results.
    """
    now = time.time()
    if _ELO_CACHE["model"] is not None and now - _ELO_CACHE["built_at"] < CACHE_TTL_SECONDS:
        return _ELO_CACHE["model"]

    client = VLRClient()
    historical_results = client.get_results()

    elo = EloModel(EloConfig())
    elo.fit(historical_results)

    _ELO_CACHE["model"] = elo
    _ELO_CACHE["built_at"] = now
    return elo

def get_upcoming_predictions() -> list[dict]:
    # instantiate the client
    client = VLRClient()
    upcoming = client.get_upcoming_matches()

    elo = build_elo_model()

    enriched_matches: list[dict] = []
    for match in upcoming:
        pred = elo.predict_match(match["team1"], match["team2"])

        enriched_matches.append({
            "match_id": match["match_id"],
            "match_event": match["event"],
            "match_series": match["series"],
            "match_page": match["match_page"],
            "teams": [match["team1"], match["team2"]],
            "time_until_match": match["time_until_match"],
            "unix_timestamp": match["unix_timestamp"],
            "predicted_winner": pred["predicted_winner"],
            "team1_win_prob": pred["team1_win_prob"],
            "team2_win_prob": pred["team2_win_prob"],
            "team1_rating": pred["team1_rating"],
            "team2_rating": pred["team2_rating"],
            "confidence": pred["confidence"],
        })

    return enriched_matches