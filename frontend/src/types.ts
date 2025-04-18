export interface News {
  title: string;
  description: string;
  date: string;
  author: string;
  url_path: string;
}

export interface Matches {
  match_event: string;
  match_page: string;
  match_series: string;
  predicted_winner: string;
  teams: [string, string];
  time_until_match: string;
}

// Past matches (results from the last 30 days)
export interface PastMatches {
	match_event: string;
	match_series: string;
	teams: [string, string];
	score1: number;
	score2: number;
	time_until_match: string;
  match_page: string;
}

// Live matches
export interface LiveMatch {
	match_event: string;
	match_series: string;
	teams: [string, string];
	team1_logo: string;
	team2_logo: string;
	score1: number;
	score2: number;
	time_started: string;
	match_page: string;
}

// export interface Stats {
//   player: string;
//   org: string;
//   rating: string;
//   average_combat_score: string;
//   kill_deaths: string;
//   kill_assists_survived_traded: string;
//   average_damage_per_round: string;
//   kills_per_round: string;
//   assists_per_round: string;
//   first_kills_per_round: string;
//   first_deaths_per_round: string;
//   headshot_percentage: string;
//   clutch_success_percentage: string;
// }

// export interface Rankings {
//   rank: string;
//   team: string;
//   country: string;
//   last_played: string;
//   last_played_team: string;
//   last_played_team_logo: string;
//   record: string;
//   earnings: string;
//   logo: string;
// }


  