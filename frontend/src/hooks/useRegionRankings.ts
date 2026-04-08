import { useEffect, useState } from 'react';
import { fetchRegionRankings } from '../api/rankings';
import { Region, RegionRankingsPayload } from '../types/api';

export function useRegionRankings(region: Region) {
  const [payload, setPayload] = useState<RegionRankingsPayload | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        setLoading(true);
        setError('');
        const data = await fetchRegionRankings(region);
        if (!cancelled) {
          setPayload(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Failed to load rankings.');
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
  }, [region]);

  return { payload, loading, error };
}
