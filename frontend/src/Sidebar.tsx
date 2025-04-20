// imports
import React from 'react';
import { Link, useLocation } from 'react-router-dom';

interface SidebarProps {
  isOpen: boolean;
  // Function to toggle sidebar
  toggle: () => void;
}

// Sidebar links
const links = [
  { to: '/',        label: 'Home',       icon: '🏠' },
  { to: '/contact', label: 'Contact Us', icon: '✉️' },
];

export default function Sidebar({ isOpen, toggle }: SidebarProps) {
  const { pathname } = useLocation();

  return (
    <div
        className="sidebar"
        style={{ width: isOpen ? '10rem' : '4rem' }} 
    >
    <button onClick={toggle}>
      {isOpen ? '☰' : '☰'}
    </button>

      <nav className="mt-4">
        {links.map(({ to, label, icon }) => (
          <Link
            key={to}
            to={to}
            className={`
              flex items-center px-4 py-2 mb-2 rounded transition-colors
              ${pathname === to
                ? 'bg-gray-700 text-white'
                : 'text-gray-300 hover:bg-gray-800'}
            `}
          >
            <span className="mr-3 text-lg">{icon}</span>
            {isOpen && <span>{label}</span>}
          </Link>
        ))}
      </nav>
    </div>
  );
}
