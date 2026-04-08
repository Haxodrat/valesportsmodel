import { NavLink } from 'react-router-dom';

export default function Sidebar() {
  return (
    <aside className="sidebar-modern">
      <NavLink to="/" end className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
        <span>Matches</span>
      </NavLink>
      <NavLink to="/rankings" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
        <span>Rankings</span>
      </NavLink>
      <NavLink to="/contact" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
        <span>Contact</span>
      </NavLink>
    </aside>
  );
}
