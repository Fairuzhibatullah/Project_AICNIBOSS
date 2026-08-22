import React from 'react';

function FuelPriceForm({ formData, setFormData }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    const parsedValue = value ? Number(value) : '';
    setFormData((prev) => ({ ...prev, [name]: parsedValue }));
  };

  return (
    <div className="form-card">
      <div className="card-header">
        <span className="material-symbols-outlined">local_gas_station</span>
        <h3>Harga BBM</h3>
      </div>
      <div className="card-body">
        <div className="form-group">
          <label>Harga BBM per Liter (Rp)</label>
          <input
            type="number"
            name="fuel_price_per_liter"
            value={formData.fuel_price_per_liter}
            onChange={handleChange}
            placeholder="13000"
            required
          />
        </div>
      </div>
    </div>
  );
}

export default FuelPriceForm;
