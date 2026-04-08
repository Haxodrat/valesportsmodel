import { Region } from '../../types/api';
import { REGIONS, labelRegion } from '../../utils/regions';

interface RegionTabsProps {
  region: Region;
  setRegion: (region: Region) => void;
}

export default function RegionTabs({ region, setRegion }: RegionTabsProps) {
  return (
    <div className="tabs">
      {REGIONS.map((value) => (
        <button
          key={value}
          className={`tab ${value === region ? 'active' : ''}`}
          onClick={() => setRegion(value)}
        >
          {labelRegion(value)}
        </button>
      ))}
    </div>
  );
}
