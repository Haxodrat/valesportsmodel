# backend/data_sources/vlr_client.py

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any
import requests

import cloudscraper
from configs.config import Config

DEFAULT_BASE_URL = Config.VLR_API_BASE_URL

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
                "Make sure the API server is running or update VLR_API_BASE_URL in .env."
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

    def get_results(self) -> list[dict]:
        """
        Returns completed matches for Elo training.
        """
        raw = self._get("/v2/match", params={"q": "results"})
        segments = raw.get("data", {}).get("segments", [])

        matches: list[dict] = []
        for m in segments:
            required = ["team1", "team2", "score1", "score2", "match_page"]
            if not all(k in m for k in required):
                continue
            score1 = self._safe_int(m.get("score1"))
            score2 = self._safe_int(m.get("score2"))
            # no scores error
            if score1 is None or score2 is None:
                continue

            team1 = self._normalize_team_name(m["team1"])
            team2 = self._normalize_team_name(m["team2"])

            winner = team1 if score1 > score2 else team2
            matches.append({
                "match_id": m.get("match_page"),
                "event": m.get("tournament_name") or m.get("match_event"),
                "series": m.get("round_info") or m.get("match_series"),
                "team1": team1,
                "team2": team2,
                "score1": score1,
                "score2": score2,
                "winner": winner,
                "completed_at": m.get("time_completed"),
                "unix_timestamp": self._safe_int(m.get("unix_timestamp")),
                "match_page": m.get("match_page"),
            })

        return matches

    @staticmethod
    def _normalize_team_name(name: str | None) -> str:
        if not name:
            return "Unknown"
        return " ".join(name.strip().split())

    @staticmethod
    def _safe_int(value: Any) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None