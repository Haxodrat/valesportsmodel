# backend/services/team_metadata.py

from __future__ import annotations

from functools import lru_cache

from data_sources.vlr_client import VLRClient


TEAM_ID_MAP: dict[str, int] = {
    # Pacific
    "Paper Rex": 624,
    "T1": 14,
    "Nongshim RedForce": 20906,
    "Rex Regum Qeon": 878,
    "DRX": 8185,
    "TALON": 8304,
    "Gen.G": 17,
    "FULL SENSE": 9187,
    "DetonatioN FocusMe": 278,
    "VARREL": 11662,
    "BOOM Esports": 773,
    "Global Esports": 918,
    "ZETA DIVISION": 5448,
    "Team Secret": 6199,

    # China
    "EDward Gaming": 1120,
    "Trace Esports": 12685,
    "All Gamers": 1119,
    "Dragon Ranger Gaming": 15763,
    "Wolves Esports": 2845,
    "Nova Esports": 15457,
    "FunPlus Phoenix": 11328,
    "Bilibili Gaming": 12010,
    "TYLOO": 731,

    # Add EMEA / Americas teams here as needed
}


def _fallback_tag(team_name: str) -> str:
    parts = team_name.replace(".", "").split()
    if not parts:
        return "TEAM"
    if len(parts) == 1:
        return parts[0][:4].upper()
    return "".join(word[0] for word in parts[:4]).upper()


@lru_cache(maxsize=256)
# cached for reduced lookups
def get_team_metadata(team_name: str) -> dict[str, str]:
    team_id = TEAM_ID_MAP.get(team_name)
    if team_id is None:
        return {
            "name": team_name,
            "tag": _fallback_tag(team_name),
            "logo": "",
        }
    client = VLRClient()

    try:
        payload = client.get_team_profile(team_id)
        info = payload.get("info", {}) if isinstance(payload, dict) else {}
        return {
            "name": info.get("name", team_name),
            "tag": info.get("tag") or _fallback_tag(team_name),
            "logo": info.get("logo", "") or "",
        }
    except Exception:
        return {
            "name": team_name,
            "tag": _fallback_tag(team_name),
            "logo": "",
        }