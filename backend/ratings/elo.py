# backend/ratings/elo.py

from __future__ import annotations

from dataclasses import dataclass, field
from math import pow
from typing import Iterable


DEFAULT_RATING = 1500.0

@dataclass
class EloConfig:
    initial_rating: float = 1500.0
    k_factor: float = 32.0
    scale: float = 400.0
    min_matches_for_confidence: int = 5


@dataclass
class TeamRatingState:
    rating: float = DEFAULT_RATING
    matches_played: int = 0


@dataclass
class EloModel:
    config: EloConfig = field(default_factory=EloConfig)
    ratings: dict[str, TeamRatingState] = field(default_factory=dict)

    def get_rating(self, team: str) -> float:
        return self.ratings.get(team, TeamRatingState(self.config.initial_rating)).rating

    def get_matches_played(self, team: str) -> int:
        return self.ratings.get(team, TeamRatingState(self.config.initial_rating)).matches_played

    def expected_score(self, rating_a: float, rating_b: float) -> float:
        return 1.0 / (1.0 + pow(10.0, (rating_b - rating_a) / self.config.scale))

    def predict_match(self, team1: str, team2: str) -> dict:
        """
        Use the elo score to predict what team wins.
        """
        r1, r2 = self.get_rating(team1), self.get_rating(team2)
        p1 = self.expected_score(r1, r2)
        p2 = 1.0 - p1
        matches1, matches2 = self.get_matches_played(team1), self.get_matches_played(team2)

        # less than min matches required
        low_data = min(matches1, matches2) < self.config.min_matches_for_confidence
        confidence = self._confidence_label(abs(p1 - 0.5), low_data)

        return {
            "team1": team1,
            "team2": team2,
            "team1_rating": round(r1, 2),
            "team2_rating": round(r2, 2),
            "team1_win_prob": round(p1, 4),
            "team2_win_prob": round(p2, 4),
            # for now just whoever has higher elo score
            "predicted_winner": team1 if p1 >= p2 else team2,
            "confidence": confidence,
            "team1_matches_played": matches1,
            "team2_matches_played": matches2,
        }

    def update_match(self, team1: str, team2: str, winner: str) -> None:
        """
        Update team's elo ratings after a match.
        """
        self._ensure_team(team1)
        self._ensure_team(team2)

        rating1, rating2 = self.ratings[team1].rating, self.ratings[team2].rating
        expected1 = self.expected_score(rating1, rating2)
        expected2 = 1.0 - expected1
        actual1 = 1.0 if winner == team1 else 0.0
        actual2 = 1.0 - actual1

        self.ratings[team1].rating = rating1 + self.config.k_factor * (actual1 - expected1)
        self.ratings[team2].rating = rating2 + self.config.k_factor * (actual2 - expected2)
        self.ratings[team1].matches_played += 1
        self.ratings[team2].matches_played += 1

    def fit(self, matches: Iterable[dict]) -> None:
        """
        Train Elo ratings chronologically.
        Expect each match dict to contain:
        team1, team2, winner, and ideally unix_timestamp.
        """
        sorted_matches = sorted(
            matches,
            key=lambda m: (
                m.get("unix_timestamp") is None,
                m.get("unix_timestamp") if m.get("unix_timestamp") is not None else 0,
                m.get("match_id", "")
            )
        )

        for match in sorted_matches:
            team1 = match["team1"]
            team2 = match["team2"]
            winner = match["winner"]
            self.update_match(team1, team2, winner)

    def _ensure_team(self, team: str) -> None:
        if team not in self.ratings:
            self.ratings[team] = TeamRatingState(rating=self.config.initial_rating, matches_played=0)

    @staticmethod
    def _confidence_label(edge_from_even: float, low_data: bool) -> str:
        if low_data:
            return "low"
        if edge_from_even >= 0.20:
            return "high"
        if edge_from_even >= 0.10:
            return "medium"
        return "low"