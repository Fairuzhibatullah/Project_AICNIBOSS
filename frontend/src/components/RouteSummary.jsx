import React from 'react';

function RouteSummary({ result }) {
  if (!result) return null;

  return (
    <div className="route-summary">
      <div className="summary-grid">
        <div className="summary-item">
          <span className="material-symbols-outlined summary-icon">route</span>
          <div className="summary-text">
            <p className="summary-label">Jarak</p>
            <p className="summary-value">{result.route.distance_km} km</p>
          </div>
        </div>
        
        <div className="summary-item">
          <span className="material-symbols-outlined summary-icon">timer</span>
          <div className="summary-text">
            <p className="summary-label">Durasi</p>
            <p className="summary-value">{result.route.duration_min} menit</p>
          </div>
        </div>
        
        <div className="summary-item">
          <span className="material-symbols-outlined summary-icon">device_thermostat</span>
          <div className="summary-text">
            <p className="summary-label">Suhu</p>
            <p className="summary-value">{result.weather.temperature_c} &deg;C</p>
          </div>
        </div>
        
        <div className="summary-item">
          <span className="material-symbols-outlined summary-icon">water_drop</span>
          <div className="summary-text">
            <p className="summary-label">Kelembapan</p>
            <p className="summary-value">{result.weather.humidity_percent}%</p>
          </div>
        </div>
        
        <div className="summary-item">
          <span className="material-symbols-outlined summary-icon">rainy</span>
          <div className="summary-text">
            <p className="summary-label">Hujan</p>
            <p className="summary-value">{result.weather.rain_mm} mm</p>
          </div>
        </div>
        
        <div className="summary-item">
          <span className="material-symbols-outlined summary-icon">speed</span>
          <div className="summary-text">
            <p className="summary-label">Konsumsi BBM</p>
            <p className="summary-value">{result.prediction.fuel_consumption_kml} km/L</p>
          </div>
        </div>
        
        <div className="summary-item">
          <span className="material-symbols-outlined summary-icon">local_gas_station</span>
          <div className="summary-text">
            <p className="summary-label">Kebutuhan BBM</p>
            <p className="summary-value">{result.fuel.fuel_needed_liter} L</p>
          </div>
        </div>
        
        <div className="summary-item highlight-item">
          <span className="material-symbols-outlined summary-icon">payments</span>
          <div className="summary-text">
            <p className="summary-label">Estimasi Biaya</p>
            <p className="summary-value highlight-text">
              {new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(result.cost.estimated_cost)}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RouteSummary;
