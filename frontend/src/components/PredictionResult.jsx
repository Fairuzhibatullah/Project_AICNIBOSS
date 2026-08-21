import React from 'react';

function PredictionResult({ result }) {
  if (!result) {
    return (
      <div className="card result-card">
        <h2>Hasil Prediksi</h2>
        <p className="placeholder-text">Silakan isi form dan klik "Prediksi Perjalanan" untuk melihat hasil.</p>
        
        <div className="result-grid">
          <div className="result-section">
            <h3>A. Rute</h3>
            <p>Jarak: - km</p>
            <p>Estimasi Durasi: - menit</p>
          </div>
          
          <div className="result-section">
            <h3>B. Cuaca</h3>
            <p>Suhu: - °C</p>
            <p>Kelembapan: - %</p>
            <p>Curah Hujan: - mm</p>
          </div>
          
          <div className="result-section">
            <h3>C. Prediksi BBM</h3>
            <p>Konsumsi BBM: - km/L</p>
          </div>
          
          <div className="result-section">
            <h3>D. Kebutuhan BBM</h3>
            <p>Kebutuhan BBM: - liter</p>
            <p>Harga BBM per liter: Rp -</p>
          </div>
          
          <div className="result-section">
            <h3>E. Estimasi Biaya</h3>
            <p className="total-cost">Total estimasi biaya: Rp -</p>
          </div>
        </div>
      </div>
    );
  }

  // Jika nanti dihubungkan dengan API, tampilkan data dari props result
  return (
    <div className="card result-card">
      <h2>Hasil Prediksi</h2>
      
      <div className="result-grid">
        <div className="result-section">
          <h3>A. Rute</h3>
          <p>Jarak: {result.route?.distance_km ?? '-'} km</p>
          <p>Estimasi Durasi: {result.route?.duration_min ?? '-'} menit</p>
        </div>
        
        <div className="result-section">
          <h3>B. Cuaca</h3>
          <p>Suhu: {result.weather?.temperature_c ?? '-'} °C</p>
          <p>Kelembapan: {result.weather?.humidity_percent ?? '-'} %</p>
          <p>Curah Hujan: {result.weather?.rain_mm ?? '-'} mm</p>
        </div>
        
        <div className="result-section">
          <h3>C. Prediksi BBM</h3>
          <p>Konsumsi BBM: {result.prediction?.fuel_consumption_kml ?? '-'} km/L</p>
        </div>
        
        <div className="result-section">
          <h3>D. Kebutuhan BBM</h3>
          <p>Kebutuhan BBM: {result.fuel?.fuel_needed_liter ?? '-'} liter</p>
          <p>Harga BBM per liter: Rp {result.fuel?.fuel_price_per_liter ?? '-'}</p>
        </div>
        
        <div className="result-section">
          <h3>E. Estimasi Biaya</h3>
          <p className="total-cost">Total estimasi biaya: Rp {result.cost?.estimated_cost ?? '-'}</p>
        </div>
      </div>
    </div>
  );
}

export default PredictionResult;
