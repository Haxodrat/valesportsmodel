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
      </div>
    </div>
  );
}
