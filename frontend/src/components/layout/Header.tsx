import { NavLink } from 'react-router-dom';

export default function Header() {
  return (
    <header className="site-header">
      <div>
        <p className="brand-kicker">VCT Model</p>
        <h1 className="brand-title">ValeSportsModel</h1>
        <p className="muted">Upcoming VCT predictions and regional Elo rankings.</p>
      </div>

      <nav className="nav-links">
        <NavLink to="/" end className={({ isActive }) => `nav-pill ${isActive ? 'active' : ''}`}>
          Matches
        </NavLink>
        <NavLink to="/rankings" className={({ isActive }) => `nav-pill ${isActive ? 'active' : ''}`}>
          Rankings
        </NavLink>
        <NavLink to="/contact" className={({ isActive }) => `nav-pill ${isActive ? 'active' : ''}`}>
          Contact
        </NavLink>
      </nav>
    </header>
  );
}
