import ErrorState from '../components/ui/ErrorState';
import LoadingState from '../components/ui/LoadingState';
import MatchList from '../components/matches/MatchList';
import { useUpcomingMatches } from '../hooks/useUpcomingMatches';

export default function HomePage() {
  const { matches, loading, error } = useUpcomingMatches();

  return (
    <section className="page">
      <div className="page-header">
        <p className="eyebrow">Upcoming matches</p>
        <h2>Valorant match predictions</h2>
        <p className="muted">
          Live upcoming VCT matches with Elo-based win probabilities and confidence spreads.
        </p>
      </div>

      {loading && <LoadingState label="Loading upcoming matches..." />}
      {error && <ErrorState message={error} />}
      {!loading && !error && <MatchList matches={matches} />}
    </section>
  );
}
