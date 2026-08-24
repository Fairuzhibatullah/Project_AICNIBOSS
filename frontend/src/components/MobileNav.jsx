import React from 'react';

function MobileNav({ showHome, onHome, onResult }) {
  return (
    <nav className="mobile-nav">
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
        <span>Hasil</span>
      </button>
    </nav>
  );
}

export default MobileNav;