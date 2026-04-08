import { UpcomingMatchPrediction } from '../../types/api';
import MatchCard from './MatchCard';

interface MatchListProps {
  matches: UpcomingMatchPrediction[];
}

export default function MatchList({ matches }: MatchListProps) {
  if (!matches.length) {
    return <div className="state-card">No supported upcoming matches found.</div>;
  }

  return (
    <div className="card-grid">
      {matches.map((match) => (
        <MatchCard key={match.match_id} match={match} />
      ))}
    </div>
  );
}
