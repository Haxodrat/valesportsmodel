export function formatPercent(probability: number): string {
  return `${(probability * 100).toFixed(1)}%`;
}

export function formatConfidence(confidence: string): string {
  return confidence.charAt(0).toUpperCase() + confidence.slice(1);
}

export function formatLastUpdated(timestamp: string): string {
  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) {
    return timestamp;
  }
  return date.toLocaleString();
}
