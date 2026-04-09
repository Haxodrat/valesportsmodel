# backend/data_sources/vlr_client.py

from __future__ import annotations

from typing import Any
import requests
from urllib.parse import urlparse

import cloudscraper
from configs.config import Config

DEFAULT_BASE_URL = Config.VLR_API_BASE_URL
TEAM_ALIASES = {
    "PCIFIC Esports": "PCIFIC",
    "BBL PCIFIC": "PCIFIC",
}

# api
class VLRClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.scraper = cloudscraper.create_scraper()

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        try:
            resp = self.scraper.get(url, params=params, timeout=20)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.ConnectionError as e:
            raise RuntimeError(
                f"Could not connect to VLR API at {self.base_url}. "
                "Make sure your self-hosted vlrggapi service is running or update VLR_API_BASE_URL in .env."
            ) from e

    def get_upcoming_matches(self) -> list[dict]:
        """
        Returns upcoming matches.
        """
        raw = self._get("/v2/match", params={"q": "upcoming"})
        segments = raw.get("data", {}).get("segments", [])

        # iterate
        matches: list[dict] = []
        for m in segments:
            if not all(k in m for k in ["team1", "team2", "match_event", "match_series", "match_page"]):
                continue
            matches.append({
                "match_id": m.get("match_page"),
                "event": m.get("match_event"),
                "series": m.get("match_series"),
                "team1": self._normalize_team_name(m.get("team1")),
                "team2": self._normalize_team_name(m.get("team2")),
                "time_until_match": m.get("time_until_match"),
                "unix_timestamp": self._safe_int(m.get("unix_timestamp")),
                "match_page": m.get("match_page"),
            })

        return matches

    def get_completed_events(self, max_pages: int = 15) -> list[dict]:
        events = []
        seen = set()

        for page in range(1, max_pages + 1):
            raw = self._get("/v2/events", params={"q": "completed", "page": page})
            segments = raw.get("data", {}).get("segments", [])

            if not segments:
                break

            for e in segments:
                url_path = e.get("url_path")
                if not url_path or url_path in seen:
                    continue
                seen.add(url_path)
                events.append(e)

        return events
    
    def _extract_event_id(self, url_path: str | None) -> str | None:
        if not url_path:
            return None

        # example: https://www.vlr.gg/event/2782/challengers-2026-emea-stage-1
        parsed = urlparse(url_path)
        parts = parsed.path.strip("/").split("/")

        for i, part in enumerate(parts):
            if part == "event" and i + 1 < len(parts):
                return parts[i + 1]
        return None
    
    def get_event_matches(self, event_id: str) -> list[dict]:
        raw = self._get("/v2/events/matches", params={"event_id": event_id})
        return raw.get("data", {}).get("segments", [])

    def _should_include_event_for_region(self, title: str | None, region: str, mode: str = "vct_only") -> bool:
        if not title:
            return False

        t = title.lower()
        region = region.lower()

        if mode == "expanded":
            return self._infer_region_from_event(title) == region

        if mode == "vct_only":
            base_2026 = f"vct 2026: {region}"
            base_2025 = f"vct 2025: {region}"

            if base_2026 in t or base_2025 in t:
                blocked = ["ascension", "game changers", "spotlight", "off//season"]
                return not any(word in t for word in blocked)

        return False
    
    def get_region_event_results(self, region: str, max_pages: int = 15, mode: str = "vct_only") -> list[dict]:
        region = region.lower().strip()
        events = self.get_completed_events(max_pages=max_pages)

        out = []
        seen_ids = set()

        for event in events:
            title = event.get("title")
            inferred = self._infer_region_from_event(title)
            if inferred != region:
                continue
        
            if not self._should_include_event_for_region(title, region, mode=mode):
                continue

            event_id = self._extract_event_id(event.get("url_path"))
            if not event_id:
                continue

            matches = self.get_event_matches(event_id)

            for m in matches:
                normalized = self._normalize_event_match(m, title)
                if normalized is None:
                    continue

                match_id = normalized["match_id"]
                if match_id in seen_ids:
                    continue

                seen_ids.add(match_id)
                out.append(normalized)

        out.sort(
            key=lambda m: (
                m.get("unix_timestamp") is None,
                m.get("unix_timestamp") if m.get("unix_timestamp") is not None else 0,
                str(m.get("match_id", "")),
            )
        )
        return out
    
    def _normalize_result_feed_match(self, m: dict[str, Any]) -> dict[str, Any] | None:
        required = ["team1", "team2", "score1", "score2", "match_page"]
        if not all(k in m for k in required):
            return None

        score1 = self._safe_int(m.get("score1"))
        score2 = self._safe_int(m.get("score2"))
        if score1 is None or score2 is None or score1 == score2:
            return None

        team1 = self._normalize_team_name(m.get("team1"))
        team2 = self._normalize_team_name(m.get("team2"))
        event_name = m.get("tournament_name") or m.get("match_event")

        winner = team1 if score1 > score2 else team2

        return {
            "match_id": m.get("match_page"),
            "event": event_name,
            "series": m.get("round_info") or m.get("match_series"),
            "team1": team1,
            "team2": team2,
            "score1": score1,
            "score2": score2,
            "winner": winner,
            "completed_at": m.get("time_completed"),
            "unix_timestamp": self._safe_int(m.get("unix_timestamp")),
            "match_page": m.get("match_page"),
            "region": self._infer_region_from_event(event_name),
        }

    def _normalize_event_match(self, m: dict[str, Any], fallback_event_name: str | None) -> dict[str, Any] | None:
        t1 = m.get("team1")
        t2 = m.get("team2")

        if not isinstance(t1, dict) or not isinstance(t2, dict):
            return None

        team1 = self._normalize_team_name(t1.get("name"))
        team2 = self._normalize_team_name(t2.get("name"))

        score1 = self._safe_int(t1.get("score"))
        score2 = self._safe_int(t2.get("score"))

        if score1 is None or score2 is None or score1 == score2:
            return None

        if t1.get("is_winner") is True:
            winner = team1
        elif t2.get("is_winner") is True:
            winner = team2
        else:
            winner = team1 if score1 > score2 else team2

        match_id = m.get("match_id")
        if not match_id:
            return None

        event_name = fallback_event_name
        return {
            "match_id": str(match_id),
            "event": event_name,
            "series": m.get("event_series"),
            "team1": team1,
            "team2": team2,
            "score1": score1,
            "score2": score2,
            "winner": winner,
            "completed_at": m.get("date"),
            "unix_timestamp": None,
            "match_page": m.get("url"),
            "region": self._infer_region_from_event(event_name),
        }

    @staticmethod
    def _normalize_team_name(name: str | None) -> str:
        if not name:
            return "Unknown"

        cleaned = " ".join(name.strip().split())
        return TEAM_ALIASES.get(cleaned, cleaned)

    @staticmethod
    def _safe_int(value: Any) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def _infer_region_from_event(self, event_name: str | None) -> str | None:
        if not event_name:
            return None

        event = event_name.lower()

        if "pacific" in event:
            return "pacific"
        if "emea" in event:
            return "emea"
        if "china" in event:
            return "china"
        if "americas" in event:
            return "americas"

        return None
    
    def get_team_profile(self, team_id: int) -> dict:
        raw = self._get("/v2/team", params={"id": team_id})
        return raw.get("data", {})