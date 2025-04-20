// imports
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Matches, News, PastMatches, LiveMatch } from './types';
import './App.css';
import { Routes, Route, Link } from 'react-router-dom';
import Contact from './Contact';
import { Analytics } from "@vercel/analytics/react";
import Sidebar from './Sidebar';

// backend URL for API requests
const BACKEND_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
// the different possible views
type View = 'past' | 'matches' | 'news' | 'live';

function App() {
	// State variables
	const [view, setView] = useState<View>('matches');
	const [matches, setMatches] = useState<Matches[]>([]);
	const [news, setNews] = useState<News[]>([]);
	const [pastMatches, setPastMatches] = useState<PastMatches[]>([]);
	const [liveMatches, setLiveMatches] = useState<LiveMatch[]>([]);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<string>('');
	const [expandedEvents, setExpandedEvents] = useState<Record<string, boolean>>({});
  const [sidebarOpen, setSidebarOpen] = useState(true);

	// Helper to build full vlr.gg URL
	const toVlrUrl = (path: string) =>
		path.startsWith('http') ? path : `https://www.vlr.gg${path}`;

	// Generic data fetcher
	const fetchData = async <T,>(
		endpoint: string,
		setter: React.Dispatch<React.SetStateAction<T[]>>
	) => {
		setLoading(true);
		setError('');
		try {
			const res = await axios.get<{ data: T[] }>(
				`${BACKEND_URL}/api/${endpoint}`
			);
			// set fetched data into state
			setter(res.data.data);
			// clear any expanded sections
			if (['upcoming-matches','past-matches','live-matches'].includes(endpoint)) {
				setExpandedEvents({});
			}
		} catch (err: any) {
			setError(err.message || 'Fetch error');
		} finally {
			setLoading(false);
		}
	};

	// Fetch when view changes
	useEffect(() => {
		switch (view) {
			case 'live':
				fetchData<LiveMatch>('live-matches', setLiveMatches);
				break;
			case 'past':
				fetchData<PastMatches>('past-matches', setPastMatches);
				break;
			case 'news':
				fetchData<News>('news', setNews);
				break;
			default:
				fetchData<Matches>('upcoming-matches', setMatches);
		}
	}, [view]);

	// Group upcoming matches by event
	const groupedMatches = matches.reduce((acc, m) => {
		(acc[m.match_event] = acc[m.match_event] || []).push(m);
		return acc;
	}, {} as Record<string, Matches[]>);

	// Filter past to last 30 days & group by event
	const recentPast = pastMatches.filter(pm => {
		const match = pm.time_until_match.match(/(\d+)([hd])/);
		if (!match) return false;
		const val = parseInt(match[1], 10);
		return match[2]==='h' || match[2]==='m' || (match[2]==='d' && val<=30);
	});
	const groupedPast = recentPast.reduce((acc, m) => {
		(acc[m.match_event] = acc[m.match_event] || []).push(m);
		return acc;
	}, {} as Record<string, PastMatches[]>);

	// Group live matches by event as well
	const groupedLive = liveMatches.reduce((acc, m) => {
		(acc[m.match_event] = acc[m.match_event] || []).push(m);
		return acc;
	}, {} as Record<string, LiveMatch[]>);

	// toggle showing a section’s table
	const toggleEvent = (event: string) =>
		setExpandedEvents(prev => ({
			...prev,
			[event]: !prev[event],
		}));

	// Render the content based on the current view
	const renderContent = () => {
		if (loading) return <div className="loading">Loading…</div>;
		if (error)   return <div className="error">Error: {error}</div>;

		if (view === 'live') {
			return (
				<div className="matches-by-event">
					{Object.entries(groupedLive).map(([event, lms]) => (
						<section key={event}>
							<h2
								className={`event-title ${
									expandedEvents[event] ? 'expanded' : ''
								}`}
								onClick={() => toggleEvent(event)}
							>
								{event}
							</h2>
							{expandedEvents[event] && (
								<table className="data-table">
									<thead>
										<tr>
											<th>Series</th>
											<th>Team 1</th>
											<th>Logo 1</th>
											<th>Score 1</th>
											<th>Score 2</th>
											<th>Logo 2</th>
											<th>Team 2</th>
											<th>Started</th>
											<th>Link</th>
										</tr>
									</thead>
									<tbody>
										{lms.map((m, i) => (
											<tr key={i}>
												<td>{m.match_series}</td>
												<td>{m.teams[0]}</td>
												<td>
													<img
														src={m.team1_logo.startsWith('//') ? 'https:' + m.team1_logo : m.team1_logo}
														alt={m.teams[0]}
														className="logo"
													/>
												</td>
												<td>{m.score1}</td>
												<td>{m.score2}</td>
												<td>
													<img
														src={m.team2_logo.startsWith('//') ? 'https:' + m.team2_logo : m.team2_logo}
														alt={m.teams[1]}
														className="logo"
													/>
												</td>
												<td>{m.teams[1]}</td>
												<td>{m.time_started}</td>
												<td>
													<a
														href={toVlrUrl(m.match_page)}
														target="_blank"
														rel="noopener noreferrer"
													>
														View on vlr.gg
													</a>
												</td>
											</tr>
										))}
									</tbody>
								</table>
							)}
						</section>
					))}
				</div>
			);
		} else if (view === 'past') {
			return (
				<div className="matches-by-event">
					{Object.entries(groupedPast).map(([event, pms]) => (
						<section key={event}>
							<h2
								className={`event-title ${
									expandedEvents[event] ? 'expanded' : ''
								}`}
								onClick={() => toggleEvent(event)}
							>
								{event}
							</h2>
							{expandedEvents[event] && (
								<table className="data-table">
									<thead>
										<tr>
											<th>Series</th>
											<th>Team 1</th>
											<th>Score 1</th>
											<th>Score 2</th>
											<th>Team 2</th>
											<th>Winner</th>
											<th>Completed</th>
											<th>Link</th>
										</tr>
									</thead>
									<tbody>
										{pms.map((m, i) => (
											<tr key={i}>
												<td>{m.match_series}</td>
												<td>{m.teams[0]}</td>
												<td>{m.score1}</td>
												<td>{m.score2}</td>
												<td>{m.teams[1]}</td>
												<td>
													{m.score1 > m.score2 ? m.teams[0] : m.teams[1]}
												</td>
												<td>{m.time_until_match}</td>
												<td>
													<a
														href={toVlrUrl(m.match_page)}
														target="_blank"
														rel="noopener noreferrer"
													>
														View on vlr.gg
													</a>
												</td>
											</tr>
										))}
									</tbody>
								</table>
							)}
						</section>
					))}
				</div>
			);
		} else if (view === 'news') {
			return (
				<div className="news-list">
					{news.map((n, i) => (
						<div key={i} className="news-item">
							<h3>
								<a
									href={n.url_path}
									target="_blank"
									rel="noopener noreferrer"
								>
									{n.title}
								</a>
							</h3>
							<p className="meta">
								{n.date} • {n.author}
							</p>
							<p>{n.description}</p>
              <a
                href={n.url_path}
                target="_blank"
                rel="noopener noreferrer"
                className="read-more"
              >
                Read more...
              </a>
						</div>
					))}
				</div>
			);
		} else {
			return (
				<div className="matches-by-event">
					{Object.entries(groupedMatches).map(([event, ms]) => (
						<section key={event}>
							<h2
								className={`event-title ${
									expandedEvents[event] ? 'expanded' : ''
								}`}
								onClick={() => toggleEvent(event)}
							>
								{event}
							</h2>
							{expandedEvents[event] && (
								<table className="data-table">
									<thead>
										<tr>
											<th>Series</th>
											<th>Teams</th>
											<th>Time</th>
											<th>Predicted Winner</th>
											<th>Link</th>
										</tr>
									</thead>
									<tbody>
										{ms.map((m, i) => (
											<tr key={i}>
												<td>{m.match_series}</td>
												<td>
													{m.teams[0]} vs {m.teams[1]}
												</td>
												<td>{m.time_until_match}</td>
												<td>{m.predicted_winner}</td>
												<td>
													<a
														href={toVlrUrl(m.match_page)}
														target="_blank"
														rel="noopener noreferrer"
													>
														View on vlr.gg
													</a>
												</td>
											</tr>
										))}
									</tbody>
								</table>
							)}
						</section>
					))}
				</div>
			);
		}
	};

	return (
    <>
      <div className="App">
        <Sidebar 
          isOpen={sidebarOpen}
          toggle={() => setSidebarOpen(open => !open)}
        />
        <div className="App-content">
          <header>
            <h1>Valorant Esports Dashboard</h1>
          </header>
          <nav className="nav">
            {(['live','past','matches','news'] as View[]).map(v => (
              <button
                key={v}
                className={`nav-button ${view === v ? 'active' : ''}`}
                onClick={() => setView(v)}
              >
                {v.charAt(0).toUpperCase() + v.slice(1)}
              </button>
            ))}
          </nav>
          <main className="flex-grow">{renderContent()}
            <Routes>
              <Route path="/contact" element={<Contact />} />
              <Route path="/" element={<div className="home">Welcome to the Valorant Esports Dashboard!</div>} />
            </Routes>
          </main>
          <footer className="footer text center py-4 text-sm text-gray-300">
            Powered by unofficial vlr.gg API
          </footer>
        </div>
        <Analytics />
      </div>
    </>
	);

}

export default App;

