import React from 'react';

function Sidebar({ showHome, onHome, onResult }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <span className="material-symbols-outlined logo-icon">
          route
        </span>

        <div className="logo-text">
          <h1>BogoRoute</h1>
          <p>AI Route Predictor</p>
        </div>
      </div>

      <nav className="sidebar-nav">
        <button
          type="button"
          className={`nav-item ${showHome ? 'active' : ''}`}
          onClick={onHome}
        >
          <span className="material-symbols-outlined">
            home
          </span>
          <span>Home</span>
        </button>

        <button
          type="button"
          className={`nav-item ${!showHome ? 'active' : ''}`}
          onClick={onResult}
        >
          <span className="material-symbols-outlined">
            analytics
          </span>
          <span>Prediksi</span>
        </button>
      </nav>
    </aside>
  );
}

export default Sidebar;