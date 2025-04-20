// src/Sidebar.tsx
import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

export default function Sidebar() {
  const [open, setOpen] = useState(true);
  const { pathname } = useLocation();

  return (
    <div
      className={
        "flex flex-col bg-gray-900 text-white h-full transition-width duration-300 " +
        (open ? "w-48" : "w-16")
      }
    >
      <button
        onClick={() => setOpen(o => !o)}
        className="self-end p-2 m-2 bg-gray-800 rounded focus:outline-none"
      >
        {open ? '←' : '→'}
      </button>

      <nav className="flex-1 mt-4">
        <Link
          to="/"
          className={
            "block px-4 py-2 rounded mb-2 transition-colors " +
            (pathname === '/' 
              ? "bg-gray-700 text-white" 
              : "text-gray-300 hover:bg-gray-800")
          }
        >
          {open ? 'Home' : '🏠'}
        </Link>
        <Link
          to="/contact"
          className={
            "block px-4 py-2 rounded mb-2 transition-colors " +
            (pathname === '/contact' 
              ? "bg-gray-700 text-white" 
              : "text-gray-300 hover:bg-gray-800")
          }
        >
          {open ? 'Contact Us' : '✉️'}
        </Link>
      </nav>
    </div>
  );
}
