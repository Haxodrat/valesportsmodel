export type Region = 'pacific' | 'emea' | 'china' | 'americas';
export type Confidence = 'low' | 'medium' | 'high';

export interface UpcomingMatchPrediction {
  match_id: string;
  match_event: string;
  match_page: string;
  match_series: string;
  predicted_winner: string;
  region: Region;
  team1: string;
  team2: string;
  teams: [string, string];
  team1_rating: number;
  team2_rating: number;
  team1_win_prob: number;
  team2_win_prob: number;
  confidence: Confidence;
  time_until_match: string;
  unix_timestamp: number | null;
}

export interface EloRankingRow {
  team: string;
  rating: number;
  matches_played: number;
}

export interface RegionRankingsPayload {
  region: Region;
  season: number;
  mode?: string;
  last_updated: string;
  training_match_count: number;
  team_count: number;
  rankings: EloRankingRow[];
}
