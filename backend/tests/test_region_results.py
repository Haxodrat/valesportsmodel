from __future__ import annotations

from data_sources.vlr_client import VLRClient


REGIONS = ["pacific", "emea", "china", "americas"]


def main():
    client = VLRClient()

    for region in REGIONS:
        matches = client.get_region_event_results(region=region, max_pages=15)

        print(f"\n=== {region.upper()} ===")
        print(f"matches: {len(matches)}")

        teams = set()
        for m in matches:
            teams.add(m["team1"])
            teams.add(m["team2"])

        print(f"unique teams: {len(teams)}")

        for m in matches[:5]:
            print(
                f"{m['team1']} vs {m['team2']} | "
                f"{m.get('event')} | "
                f"{m.get('series')} | "
                f"winner={m.get('winner')}"
            )


if __name__ == "__main__":
    main()