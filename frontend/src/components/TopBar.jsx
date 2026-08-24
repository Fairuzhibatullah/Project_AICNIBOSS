import React from 'react';

function TopBar() {
  return (
    <header className="topbar">
      <div className="topbar-brand">
        <div className="topbar-mark" aria-hidden="true">
          <span className="material-symbols-outlined">route</span>
        </div>

        <div className="topbar-content">
          <div className="topbar-eyebrow">BOGOROUTE</div>
          <p>
            Hitung estimasi konsumsi BBM berdasarkan rute dan kondisi perjalanan.
          </p>
        </div>
      </div>

      <div className="topbar-status" aria-label="Status sistem">
        <span className="status-dot"></span>
        <span>AI Route Predictor</span>
      </div>
    </header>
  );
}

export default TopBar;