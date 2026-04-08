import { formatPercent } from '../../utils/format';

interface PredictionBarProps {
  team1: string;
  team2: string;
  team1Prob: number;
  team2Prob: number;
}

export default function PredictionBar({ team1, team2, team1Prob, team2Prob }: PredictionBarProps) {
  return (
    <div className="prediction-block">
      <div className="prediction-labels">
        <span>{team1}</span>
        <span>{formatPercent(team1Prob)}</span>
      </div>

      <div className="prediction-bar" aria-hidden="true">
        <div className="prediction-fill" style={{ width: `${team1Prob * 100}%` }} />
      </div>

      <div className="prediction-labels secondary">
        <span>{team2}</span>
        <span>{formatPercent(team2Prob)}</span>
      </div>
    </div>
  );
}
