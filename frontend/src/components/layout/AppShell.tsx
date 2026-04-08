import { ReactNode } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';

interface AppShellProps {
  children: ReactNode;
}

export default function AppShell({ children }: AppShellProps) {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="app-main">
        <Header />
        <main>{children}</main>

        <footer className="site-footer">
          © {new Date().getFullYear()} Christopher Kim. All rights reserved. Data powered by{' '}
          <a
            href="https://vlrggapi.vercel.app/"
            target="_blank"
            rel="noopener noreferrer"
            className="footer-link"
          >
            vlrggapi
          </a>{' '}
          and sourced from{' '}
          <a
            href="https://www.vlr.gg/"
            target="_blank"
            rel="noopener noreferrer"
            className="footer-link"
          >
            vlr.gg
          </a>
          .
        </footer>
      </div>
    </div>
  );
}