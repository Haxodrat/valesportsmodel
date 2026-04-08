from __future__ import annotations

from services.rankings import load_region_rankings


REGIONS = ["pacific", "emea", "china", "americas"]


def main():
    for region in REGIONS:
        print(f"\n=== {region.upper()} ===")
        try:
            payload = load_region_rankings(region=region, season=2026)
        except Exception as e:
            print(f"Failed to load rankings: {e}")
            continue

        print(f"season: {payload.get('season')}")
        print(f"last_updated: {payload.get('last_updated')}")
        print(f"training_match_count: {payload.get('training_match_count')}")
        print(f"team_count: {payload.get('team_count')}")

        rankings = payload.get("rankings", [])
        if not rankings:
            print("No rankings found.")
            continue

        print("Top teams:")
        for row in rankings[:10]:
            print(f"{row['team']} | rating={row['rating']} | matches={row['matches_played']}")


if __name__ == "__main__":
    main()