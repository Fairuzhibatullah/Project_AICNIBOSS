import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import MobileNav from './components/MobileNav';
import TopBar from './components/TopBar';
import LocationForm from './components/LocationForm';
import VehicleForm from './components/VehicleForm';
import TravelConditionForm from './components/TravelConditionForm';
import FuelPriceForm from './components/FuelPriceForm';
import PredictionResult from './components/PredictionResult';
import { predictRoute } from './services/api';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    origin: 'Stasiun Bogor',
    destination: 'Kebun Raya Bogor',
    brand: 'Honda',
    model: 'Vario',
    cc: 150,
    weight_kg: 110,
    fuel_type: 'Pertamax',
    riding_style: 'Normal',
    avg_speed_kmh: 40,
    rider_weight: 70,
    city_percentage: 80,
    fuel_price_per_liter: 13000
  });

  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMsg('');
    setResult(null);
    
    try {
      const data = await predictRoute(formData);
      setResult(data);
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-layout">
      <Sidebar />
      
      <main className="main-area">
        <TopBar />
        
        <div className="content-grid">
          {/* Left Column: Form */}
          <div className="form-column">
            {errorMsg && (
              <div className="alert-error">
                <span className="material-symbols-outlined">error</span>
                <span>{errorMsg}</span>
              </div>
            )}
            
            <form onSubmit={handleSubmit} className="trip-form">
              <LocationForm formData={formData} setFormData={setFormData} />
              <VehicleForm formData={formData} setFormData={setFormData} />
              <TravelConditionForm formData={formData} setFormData={setFormData} />
              <FuelPriceForm formData={formData} setFormData={setFormData} />
              
              <button type="submit" className="btn-primary" disabled={isLoading}>
                {isLoading ? (
                  <>
                    <span className="spinner"></span>
                    Menghitung Rute...
                  </>
                ) : (
                  <>
                    <span className="material-symbols-outlined">route</span>
                    Buat Rute
                  </>
                )}
              </button>
            </form>
          </div>
          
          {/* Right Column: Map & Result */}
          <div className="result-column">
            <PredictionResult result={result} />
          </div>
        </div>
      </main>
      
      <MobileNav />
    </div>
  );
}

export default App;
