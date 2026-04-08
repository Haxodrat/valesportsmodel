import { Route, Routes } from 'react-router-dom';
import './App.css';
import AppShell from './components/layout/AppShell';
import ContactPage from './pages/ContactPage';
import HomePage from './pages/HomePage';
import RankingsPage from './pages/RankingsPage';

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/rankings" element={<RankingsPage />} />
        <Route path="/contact" element={<ContactPage />} />
      </Routes>
    </AppShell>
  );
}
