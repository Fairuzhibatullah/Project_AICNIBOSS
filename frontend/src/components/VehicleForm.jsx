import React from 'react';

function VehicleForm({ formData, setFormData }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Konversi nilai numerik
    const parsedValue = (name === 'cc' || name === 'weight_kg') ? (value ? Number(value) : '') : value;
    
    setFormData((prev) => ({ ...prev, [name]: parsedValue }));
  };

  return (
    <div className="form-card">
      <div className="card-header">
        <span className="material-symbols-outlined">two_wheeler</span>
        <h3>Spesifikasi Motor</h3>
      </div>
      <div className="card-body">
        <div className="form-row">
          <div className="form-group">
            <label>Brand</label>
            <input
              type="text"
              name="brand"
              value={formData.brand}
              onChange={handleChange}
              placeholder="Contoh: Honda"
              required
            />
          </div>
          <div className="form-group">
            <label>Model</label>
            <input
              type="text"
              name="model"
              value={formData.model}
              onChange={handleChange}
              placeholder="Contoh: Vario"
              required
            />
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Kapasitas Mesin (CC)</label>
            <input
              type="number"
              name="cc"
              value={formData.cc}
              onChange={handleChange}
              placeholder="150"
              required
            />
          </div>
          <div className="form-group">
            <label>Berat Motor (kg)</label>
            <input
              type="number"
              name="weight_kg"
              value={formData.weight_kg}
              onChange={handleChange}
              placeholder="110"
              required
            />
          </div>
        </div>
        <div className="form-group">
          <label>Jenis BBM</label>
          <input
            type="text"
            name="fuel_type"
            value={formData.fuel_type}
            onChange={handleChange}
            placeholder="Contoh: Pertamax"
            required
          />
        </div>
      </div>
    </div>
  );
}

export default VehicleForm;
