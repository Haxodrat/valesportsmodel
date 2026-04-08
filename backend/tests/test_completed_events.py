# backend/tests/test_completed_events.py

from __future__ import annotations

from data_sources.vlr_client import VLRClient


KEYWORDS = ["pacific", "emea", "china", "americas"]


def main():
    client = VLRClient()

    for page in range(1, 16):
        raw = client._get("/events", params={"q": "completed", "page": page})
        segments = raw.get("data", {}).get("segments", [])

        matches = []
        for event in segments:
            title = (event.get("title") or "").lower()
            if any(k in title for k in KEYWORDS):
                matches.append(event)

        if not matches:
            continue

        print(f"\n=== completed events page {page} ===")
        for event in matches:
            print(
                f"title={event.get('title')} | "
                f"region={event.get('region')} | "
                f"url_path={event.get('url_path')}"
            )


if __name__ == "__main__":
    main()