import React from 'react';

function VehicleForm({ formData, setFormData }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="card">
      <h2>2. Spesifikasi Motor</h2>
      <div className="form-row">
        <div className="form-group">
          <label>Brand</label>
          <input
            type="text"
            name="brand"
            value={formData.brand}
            onChange={handleChange}
            placeholder="Contoh: Honda"
          />
        </div>
        <div className="form-group">
          <label>Model</label>
          <input
            type="text"
            name="model"
            value={formData.model}
            onChange={handleChange}
            placeholder="Contoh: Vario 150"
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
          />
        </div>
        <div className="form-group">
          <label>Berat Motor (kg)</label>
          <input
            type="number"
            name="weight_kg"
            value={formData.weight_kg}
            onChange={handleChange}
            placeholder="112"
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
        />
      </div>
    </div>
  );
}

export default VehicleForm;
