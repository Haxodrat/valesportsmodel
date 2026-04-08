# backend/tests/test_rankings_vct_only.py

from __future__ import annotations

from services.rankings import load_region_rankings

REGIONS = ["pacific", "emea", "china", "americas"]

def main():
    for region in REGIONS:
        print(f"\n=== {region.upper()} ===")
        payload = load_region_rankings(region=region, season=2026, mode="vct_only")
        print(f"training_match_count: {payload.get('training_match_count')}")
        print(f"team_count: {payload.get('team_count')}")
        print("Top 5:")
        for row in payload.get("rankings", [])[:5]:
            print(f"{row['team']} | rating={row['rating']} | matches={row['matches_played']}")

if __name__ == "__main__":
    main()