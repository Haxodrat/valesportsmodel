// src/Dashboard.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Matches, News, PastMatches, LiveMatch } from './types';
// …all your fetchData, useEffect, renderContent, etc…
export default function Dashboard() {
  // copy your existing state/hooks and renderContent logic here
  // but remove <Analytics />, <Sidebar />, and <Routes /> logic
  return (
    <div className="mx-auto max-w-4xl">
      {/* your header, top nav buttons (Live/Past/Matches/News), and renderContent() */}
    </div>
  );
}
