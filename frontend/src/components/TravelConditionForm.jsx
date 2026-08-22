import React from 'react';

function TravelConditionForm({ formData, setFormData }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Konversi nilai numerik
    const numericFields = ['avg_speed_kmh', 'rider_weight', 'city_percentage'];
    const parsedValue = numericFields.includes(name) ? (value ? Number(value) : '') : value;
    
    setFormData((prev) => ({ ...prev, [name]: parsedValue }));
  };

  return (
    <div className="form-card">
      <div className="card-header">
        <span className="material-symbols-outlined">speed</span>
        <h3>Kondisi Perjalanan</h3>
      </div>
      <div className="card-body">
        <div className="form-row">
          <div className="form-group">
            <label>Gaya Berkendara</label>
            <select className="select-input" name="riding_style" value={formData.riding_style} onChange={handleChange} required>
              <option value="Normal">Normal</option>
              <option value="Agresif">Agresif</option>
              <option value="Santai">Santai</option>
            </select>
          </div>
          <div className="form-group">
            <label>Kec. Rata-rata (km/jam)</label>
            <input
              type="number"
              name="avg_speed_kmh"
              value={formData.avg_speed_kmh}
              onChange={handleChange}
              placeholder="40"
              required
            />
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Berat Pengendara (kg)</label>
            <input
              type="number"
              name="rider_weight"
              value={formData.rider_weight}
              onChange={handleChange}
              placeholder="70"
              required
            />
          </div>
          <div className="form-group">
            <label>Dalam Kota (%)</label>
            <input
              type="number"
              name="city_percentage"
              value={formData.city_percentage}
              onChange={handleChange}
              placeholder="80"
              required
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default TravelConditionForm;
