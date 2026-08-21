import React, { useState } from 'react';
import Header from './components/Header';
import LocationForm from './components/LocationForm';
import VehicleForm from './components/VehicleForm';
import TravelConditionForm from './components/TravelConditionForm';
import FuelPriceForm from './components/FuelPriceForm';
import PredictionResult from './components/PredictionResult';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    origin: '',
    destination: '',
    brand: '',
    model: '',
    cc: '',
    weight_kg: '',
    fuel_type: '',
    riding_style: 'Normal',
    avg_speed_kmh: '',
    rider_weight: '',
    city_percentage: '',
    fuel_price_per_liter: ''
  });

  const [result, setResult] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Placeholder function, tidak melakukan fetch ke API
    console.log("Form dikirim:", formData);
    
    // Simulasi loading atau berhasil (saat ini cukup alert atau biarkan konsol)
    alert("Tombol Prediksi ditekan! (Fitur integrasi API belum aktif)");
  };

  return (
    <div className="app-container">
      <Header />
      
      <main className="main-content">
        <div className="form-section">
          <form onSubmit={handleSubmit}>
            <LocationForm formData={formData} setFormData={setFormData} />
            <VehicleForm formData={formData} setFormData={setFormData} />
            <TravelConditionForm formData={formData} setFormData={setFormData} />
            <FuelPriceForm formData={formData} setFormData={setFormData} />
            
            <button type="submit" className="btn-predict">
              Prediksi Perjalanan
            </button>
          </form>
        </div>
        
        <div className="result-section-container">
          <PredictionResult result={result} />
        </div>
      </main>
    </div>
  );
}

export default App;
