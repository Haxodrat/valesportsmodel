import { useEffect, useState } from 'react';
import { fetchUpcomingMatches } from '../api/matches';
import { UpcomingMatchPrediction } from '../types/api';

export function useUpcomingMatches() {
  const [matches, setMatches] = useState<UpcomingMatchPrediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        setLoading(true);
        setError('');
        const data = await fetchUpcomingMatches();
        if (!cancelled) {
          setMatches(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Failed to load upcoming matches.');
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  return { matches, loading, error };
}
