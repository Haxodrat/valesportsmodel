import { TeamInfo } from '../../types/api';

interface TeamIdentityProps {
  team: TeamInfo;
  compact?: boolean;
  showTag?: boolean;
}

export default function TeamIdentity({
  team,
  compact = false,
  showTag = true,
}: TeamIdentityProps) {
  return (
    <span className={`team-identity ${compact ? 'compact' : ''}`}>
      {team.logo ? (
        <img className="team-logo" src={team.logo} alt={team.name} />
      ) : (
        <span className="team-logo team-logo-fallback" aria-hidden="true">
          {team.tag?.slice(0, 1) || team.name.slice(0, 1)}
        </span>
      )}

      <span className="team-name-text">{team.name}</span>

      {showTag && <span className="team-tag">{team.tag}</span>}
    </span>
  );
}