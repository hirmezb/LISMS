import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import Dashboard from './pages/Dashboard';
import SamplesPage from './pages/SamplesPage';
import EquipmentPage from './pages/EquipmentPage';
import HistoryPage from './pages/HistoryPage';

/**
 * Main application component that wires together the router and pages.
 */
function App() {
  return (
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/samples" element={<SamplesPage />} />
        <Route path="/equipment" element={<EquipmentPage />} />
        <Route path="/history" element={<HistoryPage />} />
      </Routes>
    </Router>
  );
}

export default App;