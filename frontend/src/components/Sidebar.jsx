import React from 'react';

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <span className="material-symbols-outlined logo-icon">route</span>
        <div className="logo-text">
          <h1>BogoRoute</h1>
          <p>AI Route Predictor</p>
        </div>
      </div>
      
      <nav className="sidebar-nav">
        <a href="#" className="nav-item">
          <span className="material-symbols-outlined">home</span>
          <span>Beranda</span>
        </a>
        <a href="#" className="nav-item active">
          <span className="material-symbols-outlined">directions_car</span>
          <span>Hasil</span>
        </a>
        <a href="#" className="nav-item">
          <span className="material-symbols-outlined">analytics</span>
          <span>Hasil Prediksi</span>
        </a>
        <a href="#" className="nav-item">
          <span className="material-symbols-outlined">info</span>
          <span>Tentang</span>
        </a>
      </nav>
    </aside>
  );
}

export default Sidebar;
