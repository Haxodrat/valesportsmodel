import { Region } from '../types/api';

export const REGIONS: Region[] = ['pacific', 'emea', 'china', 'americas'];

export function labelRegion(region: Region): string {
  switch (region) {
    case 'pacific':
      return 'Pacific';
    case 'emea':
      return 'EMEA';
    case 'china':
      return 'China';
    case 'americas':
      return 'Americas';
    default:
      return region;
  }
}
