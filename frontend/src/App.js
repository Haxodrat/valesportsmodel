// src/App.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  // vars
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // get backend data
    axios.get('http://localhost:8000/api/upcoming-matches')
      .then(res => {
        // expect the data from the backend to be in { data: [match, ...] }
        setMatches(res.data.data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message || "Error fetching matches");
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="loading">Loading upcoming matches...</div>;
  if (error) return <div className="error">Error: {error}</div>;

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
              {matches.map((match, idx) => (
                <tr key={idx}>
                  <td>
                    <a href={match.match_page} target="_blank" rel="noopener noreferrer">
                      {match.match_event}
                    </a>
                  </td>
                  <td>{match.match_series}</td>
                  <td>{match.teams[0]} vs {match.teams[1]}</td>
                  <td>{match.time_until_match}</td>
                  <td>{match.predicted_winner}</td>
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
