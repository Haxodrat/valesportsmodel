import { apiGet } from './client';
import { Region, RegionRankingsPayload } from '../types/api';

export async function fetchRegionRankings(region: Region): Promise<RegionRankingsPayload> {
  return apiGet<RegionRankingsPayload>(`/rankings/${region}`);
}
