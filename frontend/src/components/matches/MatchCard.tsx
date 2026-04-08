import Badge from '../ui/Badge';
import PredictionBar from './PredictionBar';
import { UpcomingMatchPrediction } from '../../types/api';
import { formatConfidence } from '../../utils/format';
import { labelRegion } from '../../utils/regions';

interface MatchCardProps {
  match: UpcomingMatchPrediction;
}

function toVlrUrl(path: string): string {
  if (!path) {
    return '#';
  }

  return path.startsWith('http') ? path : `https://www.vlr.gg/${path.replace(/^\/+/, '')}`;
}

export default function MatchCard({ match }: MatchCardProps) {
  const matchUrl = toVlrUrl(match.match_page);

  return (
    <article className="card">
      <div className="card-top">
        <div>
          <p className="eyebrow">{labelRegion(match.region)}</p>

          <h3 className="card-title">
            <a
              className="match-title-link"
              href={matchUrl}
              target="_blank"
              rel="noopener noreferrer"
              title={`Open ${match.team1} vs ${match.team2} on vlr.gg`}
            >
              {match.team1} vs {match.team2}
            </a>
          </h3>

          <p className="muted">
            {match.match_event} · {match.match_series}
          </p>
        </div>

        <div className="badge-row">
          <Badge tone="default">{formatConfidence(match.confidence)}</Badge>
          <Badge tone="accent">{match.time_until_match}</Badge>
        </div>
      </div>

      <PredictionBar
        team1={match.team1}
        team2={match.team2}
        team1Prob={match.team1_win_prob}
        team2Prob={match.team2_win_prob}
      />

      <div className="card-footer">
        <span>
          Predicted winner: <strong>{match.predicted_winner}</strong>
        </span>
        <span className="muted">
          Elo: {match.team1_rating} / {match.team2_rating}
        </span>
      </div>
    </article>
  );
}