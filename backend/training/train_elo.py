# backend/training/train_elo.py

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone

from data_sources.vlr_client import VLRClient
from ratings.elo import EloModel, EloConfig


REGIONS = ["pacific", "emea", "china", "americas"]
DEFAULT_MODE = "vct_only"


def train_region(region: str, max_pages: int = 20, mode: str = DEFAULT_MODE) -> dict:
    client = VLRClient()
    matches = client.get_region_event_results(
        region=region, 
        max_pages=max_pages,
        mode=mode,
    )
    elo = EloModel(
        EloConfig(
            initial_rating=1500.0,
            k_factor=32.0,
            scale=400.0,
            min_matches_for_confidence=5,
        )
    )
    elo.fit(matches)


    payload = {
        "region": region,
        "season": 2026,
        "mode": mode,
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "training_match_count": len(matches),
        "team_count": len(elo.ratings),
        "elo_model": elo.to_dict(),
        "rankings": elo.get_rankings(),
    }
    return payload


def save_region_payload(payload: dict) -> Path:
    out_dir = Path("data/elo")
    out_dir.mkdir(parents=True, exist_ok=True)

    region = payload["region"]
    season = payload["season"]
    mode = payload.get("mode", "default")
    out_path = out_dir / f"{region}_{season}_{mode}.json"

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    return out_path


def main():
    # go through regions and build the data
    for region in REGIONS:
        payload = train_region(region=region, max_pages=15, mode=DEFAULT_MODE)
        out_path = save_region_payload(payload)

        print(
            f"Saved {region} -> {out_path} | "
            f"{payload['training_match_count']} matches | "
            f"{payload['team_count']} teams | "
            f"mode={payload['mode']}"
        )


if __name__ == "__main__":
    main()