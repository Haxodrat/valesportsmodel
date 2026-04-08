# backend/services/rankings.py

from __future__ import annotations

import json
from pathlib import Path

from services.team_metadata import get_team_metadata


MIN_MATCHES_FOR_RANKINGS = 2


def load_region_rankings(region: str, season: int = 2026, mode: str = "vct_only") -> dict:
    path = Path("data/elo") / f"{region}_{season}_{mode}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"No Elo ranking file found for region={region}, season={season}, mode={mode}"
        )

    payload = json.loads(path.read_text(encoding="utf-8"))

    filtered_rankings = [
        row for row in payload.get("rankings", [])
        if row.get("matches_played", 0) >= MIN_MATCHES_FOR_RANKINGS
    ]

    payload["rankings"] = [
        {
            **row,
            "team_info": get_team_metadata(row["team"]),
        }
        for row in filtered_rankings
    ]
    payload["team_count"] = len(filtered_rankings)

    return payload