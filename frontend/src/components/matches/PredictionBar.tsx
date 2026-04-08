import { formatPercent } from '../../utils/format';
import { TeamInfo } from '../../types/api';
import TeamIdentity from '../ui/TeamIdentity';

interface PredictionBarProps {
  team1: TeamInfo;
  team2: TeamInfo;
  team1Prob: number;
  team2Prob: number;
}

export default function PredictionBar({ team1, team2, team1Prob, team2Prob }: PredictionBarProps) {
  return (
    <div className="prediction-block">
      <div className="prediction-labels">
        <TeamIdentity team={team1} compact />
        <span>{formatPercent(team1Prob)}</span>
      </div>

      <div className="prediction-bar" aria-hidden="true">
        <div className="prediction-fill" style={{ width: `${team1Prob * 100}%` }} />
      </div>

      <div className="prediction-labels secondary">
        <TeamIdentity team={team2} compact />
        <span>{formatPercent(team2Prob)}</span>
      </div>
    </div>
  );
}