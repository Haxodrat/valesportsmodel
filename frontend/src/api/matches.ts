import { apiGet } from './client';
import { UpcomingMatchPrediction } from '../types/api';

interface UpcomingMatchesResponse {
  data: UpcomingMatchPrediction[];
}

export async function fetchUpcomingMatches(): Promise<UpcomingMatchPrediction[]> {
  const json = await apiGet<UpcomingMatchesResponse>('/upcoming-matches');
  return json.data ?? [];
}
