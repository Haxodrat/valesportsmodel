# backend/services/rankings.py

from __future__ import annotations

import json
from pathlib import Path


def load_region_rankings(region: str, season: int = 2026, mode: str = "vct_only") -> dict:
    path = Path("data/elo") / f"{region}_{season}_{mode}.json"
    if not path.exists():
        raise FileNotFoundError(f"No Elo ranking file found for region={region}, season={season}, mode={mode}")
    return json.loads(path.read_text(encoding="utf-8"))