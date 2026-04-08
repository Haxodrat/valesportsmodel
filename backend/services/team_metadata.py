from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from data_sources.vlr_client import VLRClient


TEAM_IDS_PATH = Path("data/team_ids.json")


@lru_cache(maxsize=1)
def load_team_id_map() -> dict[str, int]:
    payload = json.loads(TEAM_IDS_PATH.read_text(encoding="utf-8"))

    flat: dict[str, int] = {}
    for region_map in payload.values():
        flat.update(region_map)

    return flat


def _fallback_tag(team_name: str) -> str:
    parts = team_name.replace(".", "").split()
    if not parts:
        return "TEAM"
    if len(parts) == 1:
        return parts[0][:4].upper()
    return "".join(word[0] for word in parts[:4]).upper()


@lru_cache(maxsize=256)
def get_team_metadata(team_name: str) -> dict[str, str]:
    team_id_map = load_team_id_map()
    team_id = team_id_map.get(team_name)

    if team_id is None:
        return {
            "name": team_name,
            "tag": _fallback_tag(team_name),
            "logo": "",
        }

    client = VLRClient()

    try:
        payload = client.get_team_profile(team_id)
        segments = payload.get("segments", []) if isinstance(payload, dict) else []
        team = segments[0] if segments else {}

        return {
            "name": team_name,
            "tag": team.get("tag") or _fallback_tag(team_name),
            "logo": team.get("logo", "") or "",
        }
    except Exception:
        return {
            "name": team_name,
            "tag": _fallback_tag(team_name),
            "logo": "",
        }