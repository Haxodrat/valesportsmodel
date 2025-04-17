// imports
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Matches,
  News,
  Stats,
  Rankings,
} from './types';
import './App.css';

// url to grab data
const BACKEND_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// the different views in the dashboard
type View = 'matches' | 'news' | 'stats' | 'rankings';

function App() {
  // states and vars
  const [view, setView] = useState<View>('matches');
  const [matches, setMatches] = useState<Matches[]>([]);
  const [news, setNews] = useState<News[]>([]);
  const [stats, setStats] = useState<Stats[]>([]);
  const [rankings, setRankings] = useState<Rankings[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [expandedEvents, setExpandedEvents] = useState<Record<string, boolean>>({});

  // grab the data
  const fetchData = async <T,>(endpoint: string, setter: React.Dispatch<React.SetStateAction<T[]>>) => {
    setLoading(true);
    setError('');
    try {
      const res = await axios.get<{ data: T[] }>(`${BACKEND_URL}/api/${endpoint}`);
      setter(res.data.data);
      // reset expanded when new data arrives
      if (endpoint === 'upcoming-matches') {
        setExpandedEvents({});
      }
    } catch (err: any) {
      setError(err.message || 'Fetch error');
    } finally {
      setLoading(false);
    }
  };

  // show data dependent on the view selected
  useEffect(() => {
    switch (view) {
      case 'matches':
        fetchData<Matches>('upcoming-matches', setMatches);
        break;
      case 'news':
        fetchData<News>('news', setNews);
        break;
      case 'stats':
        fetchData<Stats>('stats?region=na&timespan=all', setStats);
        break;
      case 'rankings':
        fetchData<Rankings>('rankings?region=na', setRankings);
        break;
    }
  }, [view]);

  const groupedMatches = matches.reduce((acc, m) => {
    (acc[m.match_event] = acc[m.match_event] || []).push(m);
    return acc;
  }, {} as Record<string, Matches[]>);

  const toggleEvent = (event: string) => {
    setExpandedEvents(prev => ({
      ...prev,
      [event]: !prev[event]
    }));
  };

  const renderContent = () => {
    if (loading) return <div className="loading">Loading…</div>;
    if (error)   return <div className="error">Error: {error}</div>;

    switch (view) {
      case 'matches':
        return (
          <div className="matches-by-event">
            {Object.entries(groupedMatches).map(([event, ms]) => (
              <section key={event}>
                <h2
                  className={`event-title ${expandedEvents[event] ? 'expanded' : ''}`}
                  onClick={() => toggleEvent(event)}
                >
                  {event}
                </h2>
                {expandedEvents[event] && (
                  <table className="data-table">
                    <thead>
                      <tr><th>Series</th><th>Teams</th><th>Time</th><th>Winner</th></tr>
                    </thead>
                    <tbody>
                      {ms.map((m, i) => (
                        <tr key={i}>
                          <td>{m.match_series}</td>
                          <td>{m.teams[0]} vs {m.teams[1]}</td>
                          <td>{m.time_until_match}</td>
                          <td>{m.predicted_winner}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </section>
            ))}
          </div>
        );
      case 'news':
        return (
          <div className="news-list">
            {news.map((n, i) => (
              <div key={i} className="news-item">
                <h3>
                  <a href={n.url_path} target="_blank" rel="noopener noreferrer">
                    {n.title}
                  </a>
                </h3>
                <p className="meta">{n.date} • {n.author}</p>
                <p>{n.description}</p>
              </div>
            ))}
          </div>
        );
      case 'stats':
        return (
          <table className="data-table">
            <thead>
              <tr>
                <th>Player</th><th>Org</th><th>Rating</th><th>ACS</th><th>K/D</th><th>ADR</th>
              </tr>
            </thead>
            <tbody>
              {stats.map((s, i) => (
                <tr key={i}>
                  <td>{s.player}</td>
                  <td>{s.org}</td>
                  <td>{s.rating}</td>
                  <td>{s.average_combat_score}</td>
                  <td>{s.kill_deaths}</td>
                  <td>{s.average_damage_per_round}</td>
                </tr>
              ))}
            </tbody>
          </table>
        );
      case 'rankings':
        return (
          <table className="data-table">
            <thead>
              <tr>
                <th>Rank</th><th>Team</th><th>Country</th><th>Record</th><th>Earnings</th>
              </tr>
            </thead>
            <tbody>
              {rankings.map((r, i) => (
                <tr key={i}>
                  <td>{r.rank}</td>
                  <td>{r.team}</td>
                  <td>{r.country}</td>
                  <td>{r.record}</td>
                  <td>{r.earnings}</td>
                </tr>
              ))}
            </tbody>
          </table>
        );
      default:
        return null;
    }
  };

  return (
    <div className="App">
      <header><h1>Valorant Esports Dashboard</h1></header>
      <nav className="nav">
        {(['matches','news','stats','rankings'] as View[]).map(v => (
          <button
            key={v}
            className={`nav-button ${view===v ? 'active' : ''}`}
            onClick={() => setView(v)}>
            {v.charAt(0).toUpperCase() + v.slice(1)}
          </button>
        ))}
      </nav>
      <main>{renderContent()}</main>
    </div>
  );
}

export default App;
