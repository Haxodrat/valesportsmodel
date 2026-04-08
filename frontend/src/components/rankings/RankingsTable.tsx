import { EloRankingRow } from '../../types/api';
import TeamIdentity from '../ui/TeamIdentity';

interface RankingsTableProps {
  rankings?: EloRankingRow[];
}

export default function RankingsTable({ rankings = [] }: RankingsTableProps) {
  return (
    <div className="table-wrap">
      <table className="rankings-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Team</th>
            <th>Rating</th>
            <th>Matches</th>
          </tr>
        </thead>
        <tbody>
          {rankings.map((row, index) => (
            <tr key={row.team}>
              <td>{index + 1}</td>
              <td>
                <TeamIdentity team={row.team_info} />
              </td>
              <td>{row.rating}</td>
              <td>{row.matches_played}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}