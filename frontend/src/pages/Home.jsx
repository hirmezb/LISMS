import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css';

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <h1 className="home-title">LISMS Dashboard</h1>
      <div className="home-grid">
        <button className="home-button" onClick={() => navigate('/equipment')}>Equipment</button>
        <button className="home-button" onClick={() => navigate('/inventory')}>Inventory</button>
        <button className="home-button" onClick={() => navigate('/locations')}>Locations</button>
        <button className="home-button" onClick={() => navigate('/samples')}>Samples</button>
        <button className="home-button" onClick={() => navigate('/tests')}>Tests</button>
      </div>
    </div>
  );
}

export default Home;
