// imports
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Match } from './types';
import './App.css';

// the url to pull data from
const BACKEND_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  // states, vars
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    axios
      .get<{ data: Match[] }>(`${BACKEND_URL}/api/upcoming-matches`)
      .then(res => {
        setMatches(res.data.data);
      })
      // failed to get matches
      .catch(err => {
        setError(err.message || 'Error fetching matches');
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  // loading state
  if (loading) return <div className="loading">Loading upcoming matches…</div>;
  // error state
  if (error)   return <div className="error">Error: {error}</div>;

  return (
    <div className="App">
      <header>
        <h1>Upcoming Valorant Matches</h1>
      </header>
      <main>
        {matches.length > 0 ? (
          <table className="matches-table">
            <thead>
              <tr>
                <th>Match Event</th>
                <th>Match Series</th>
                <th>Teams</th>
                <th>Time Until Match</th>
                <th>Predicted Winner</th>
              </tr>
            </thead>
            <tbody>
              {matches.map((m, i) => (
                <tr key={i}>
                  <td>
                    <a href={m.match_page} target="_blank" rel="noopener noreferrer">
                      {m.match_event}
                    </a>
                  </td>
                  <td>{m.match_series}</td>
                  <td>{m.teams[0]} vs {m.teams[1]}</td>
                  <td>{m.time_until_match}</td>
                  <td>{m.predicted_winner}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No match data available at the moment.</p>
        )}
      </main>
    </div>
  );
}

export default App;
