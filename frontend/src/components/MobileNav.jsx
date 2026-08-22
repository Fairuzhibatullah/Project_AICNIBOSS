import React from 'react';

function MobileNav() {
  return (
    <nav className="mobile-nav">
      <a href="#" className="nav-item">
        <span className="material-symbols-outlined">home</span>
        <span>Beranda</span>
      </a>
      <a href="#" className="nav-item active">
        <span className="material-symbols-outlined">directions_car</span>
        <span>Perjalanan</span>
      </a>
      <a href="#" className="nav-item">
        <span className="material-symbols-outlined">analytics</span>
        <span>Hasil</span>
      </a>
      <a href="#" className="nav-item">
        <span className="material-symbols-outlined">info</span>
        <span>Tentang</span>
      </a>
    </nav>
  );
}

export default MobileNav;
