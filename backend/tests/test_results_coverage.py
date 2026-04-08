# backend/tests/test_results_coverage.py

from data_sources.vlr_client import VLRClient


def main():
    client = VLRClient()
    matches = client.get_results(max_pages=15)

    print(f"Total normalized completed matches: {len(matches)}")
    print()

    for m in matches[:5]:
        print(m)

    print()
    unique_teams = set()
    for m in matches:
        unique_teams.add(m["team1"])
        unique_teams.add(m["team2"])

    print(f"Unique teams in training data: {len(unique_teams)}")


if __name__ == "__main__":
    main()