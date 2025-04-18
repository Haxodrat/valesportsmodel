// imports
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Matches, News, PastMatches } from './types';
import './App.css';

// backend URL for API requests
const BACKEND_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
// the different possible views
type View = 'past' | 'matches' | 'news';

function App() {
  // State variables
	const [view, setView] = useState<View>('matches');
	const [matches, setMatches] = useState<Matches[]>([]);
	const [news, setNews] = useState<News[]>([]);
	const [pastMatches, setPastMatches] = useState<PastMatches[]>([]);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<string>('');
	const [expandedEvents, setExpandedEvents] = useState<Record<string, boolean>>({});

	// Helper to build full vlr.gg URL
	const toVlrUrl = (path: string) =>
		path.startsWith('http') ? path : `https://www.vlr.gg${path}`;

	// data fetcher
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
      // for matches, set the teams to be a string array
			setter(res.data.data);
			if (endpoint === 'upcoming-matches' || endpoint === 'past-matches') {
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
		if (view === 'past') {
      fetchData<PastMatches>('past-matches', setPastMatches);
		} else if (view === 'news') {
			fetchData<News>('news', setNews);
		} else {
      fetchData<Matches>('upcoming-matches', setMatches);
		}
	}, [view]);

	// Group upcoming matches by event
	const groupedMatches = matches.reduce((acc, m) => {
		(acc[m.match_event] = acc[m.match_event] || []).push(m);
		return acc;
	}, {} as Record<string, Matches[]>);

	// Filter past matches to only last 30 days
	const recentPast = pastMatches.filter(pm => {
		const tc = pm.time_until_match;
		const match = tc.match(/(\d+)([hd])/);
		if (match) {
      // parser for time until match
			const val = parseInt(match[1], 10);
			const unit = match[2];
			if (unit === 'h' || unit === 'm') return true;
			if (unit === 'd' && val <= 30) return true;
		}
		return false;
	});

	// Group recent past matches by event
	const groupedPast = recentPast.reduce((acc, m) => {
		(acc[m.match_event] = acc[m.match_event] || []).push(m);
		return acc;
	}, {} as Record<string, PastMatches[]>);

	const toggleEvent = (event: string) =>
		setExpandedEvents(prev => ({
			...prev,
			[event]: !prev[event],
		}));

  // Render the content based on the current view
	const renderContent = () => {
		if (loading) return <div className="loading">Loading…</div>;
		if (error) return <div className="error">Error: {error}</div>;

		if (view === 'past') {
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
											<th>Teams & Scores</th>
											<th>Winner</th>
											<th>Completed</th>
											<th>Link</th>
										</tr>
									</thead>
									<tbody>
										{pms.map((m, i) => (
											<tr key={i}>
												<td>{m.match_series}</td>
												<td>
													{m.teams[0]} {m.score1} - {m.score2}{' '}
													{m.teams[1]}
												</td>
												<td>
													{m.score1 > m.score2
														? m.teams[0]
														: m.teams[1]}
												</td>
												<td>{m.time_until_match}</td>
												<td>
													<a
														href={toVlrUrl(m.match_page)}
														target="_blank"
														rel="noopener noreferrer"
													>
														View on VLR.gg
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
														View on VLR.gg
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
		<div className="App">
			<header>
				<h1>Valorant Esports Dashboard</h1>
			</header>
			<nav className="nav">
				{(['past', 'matches', 'news'] as View[]).map(v => (
					<button
						key={v}
						className={`nav-button ${view === v ? 'active' : ''}`}
						onClick={() => setView(v)}
					>
						{v.charAt(0).toUpperCase() + v.slice(1)}
					</button>
				))}
			</nav>
			<main>{renderContent()}</main>
		</div>
	);
}

export default App;
