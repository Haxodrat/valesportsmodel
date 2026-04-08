# backend/services/predictions.py

from __future__ import annotations

import json
from pathlib import Path

from data_sources.vlr_client import VLRClient
from ratings.elo import EloModel


def load_region_elo_model(region: str, season: int = 2026, mode: str = "vct_only") -> EloModel:
    path = Path("data/elo") / f"{region}_{season}_{mode}.json"    
    if not path.exists():
        raise FileNotFoundError(f"No saved Elo file found for {region} {season}")

    payload = json.loads(path.read_text(encoding="utf-8"))
    return EloModel.from_dict(payload["elo_model"])


def get_upcoming_predictions(season: int = 2026, mode: str = "vct_only") -> list[dict]:
    client = VLRClient()
    upcoming = client.get_upcoming_matches()

    enriched_matches: list[dict] = []

    for match in upcoming:
        region = client._infer_region_from_event(match.get("event"))
        if region is None:
            continue

        try:
            elo = load_region_elo_model(region=region, season=season, mode=mode)
        except FileNotFoundError:
            continue

        team1 = match["team1"]
        team2 = match["team2"]
        pred = elo.predict_match(team1, team2)

        enriched_matches.append({
            "match_id": match["match_id"],
            "match_event": match["event"],
            "match_series": match["series"],
            "match_page": match["match_page"],
            "region": region,
            "team1": team1,
            "team2": team2,
            "teams": [team1, team2],
            "time_until_match": match["time_until_match"],
            "unix_timestamp": match["unix_timestamp"],
            "predicted_winner": pred["predicted_winner"],
            "team1_win_prob": pred["team1_win_prob"],
            "team2_win_prob": pred["team2_win_prob"],
            "team1_rating": pred["team1_rating"],
            "team2_rating": pred["team2_rating"],
            "confidence": pred["confidence"],
        })

    enriched_matches.sort(
        key=lambda m: (
            m.get("unix_timestamp") is None,
            m.get("unix_timestamp") if m.get("unix_timestamp") is not None else 0,
            m.get("match_id", ""),
        )
    )

    return enriched_matches