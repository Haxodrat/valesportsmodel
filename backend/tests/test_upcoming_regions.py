from __future__ import annotations

from data_sources.vlr_client import VLRClient


def main():
    client = VLRClient()
    matches = client.get_upcoming_matches()

    print(f"upcoming matches fetched: {len(matches)}")

    counts = {}
    for m in matches:
        region = client._infer_region_from_event(m.get("event"))
        counts[region] = counts.get(region, 0) + 1

    print("\nRegion counts:")
    for region, count in sorted(counts.items(), key=lambda x: str(x[0])):
        print(f"{region}: {count}")

    print("\nSample upcoming matches:")
    for m in matches[:15]:
        region = client._infer_region_from_event(m.get("event"))
        print(
            f"{m['team1']} vs {m['team2']} | "
            f"{m.get('event')} | "
            f"region={region}"
        )


if __name__ == "__main__":
    main()