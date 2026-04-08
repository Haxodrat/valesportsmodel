import { useState } from 'react';
import ErrorState from '../components/ui/ErrorState';
import LoadingState from '../components/ui/LoadingState';
import RankingsTable from '../components/rankings/RankingsTable';
import RegionTabs from '../components/rankings/RegionTabs';
import { useRegionRankings } from '../hooks/useRegionRankings';
import { Region } from '../types/api';
import { formatLastUpdated } from '../utils/format';
import { labelRegion } from '../utils/regions';

export default function RankingsPage() {
  const [region, setRegion] = useState<Region>('pacific');
  const { payload, loading, error } = useRegionRankings(region);

  return (
    <section className="page">
      <div className="page-header">
        <p className="eyebrow">Regional Elo rankings</p>
        <h2>{labelRegion(region)} rankings</h2>
        <p className="muted">Compact VCT-focused Elo snapshots for the 2026 season.</p>
      </div>

      <RegionTabs region={region} setRegion={setRegion} />

      {loading && <LoadingState label="Loading rankings..." />}
      {error && <ErrorState message={error} />}
      {!loading && !error && payload && (
        <>
          <div className="meta-row">
            <span>Matches: {payload.training_match_count}</span>
            <span>Teams: {payload.team_count}</span>
            <span>Updated: {formatLastUpdated(payload.last_updated)}</span>
          </div>
          <RankingsTable rankings={payload.rankings} />
        </>
      )}
    </section>
  );
}
