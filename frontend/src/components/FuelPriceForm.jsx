import React from 'react';

function FuelPriceForm({ formData, setFormData }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="card">
      <h2>4. Harga BBM</h2>
      <div className="form-group">
        <label>Harga BBM per Liter (Rp)</label>
        <input
          type="number"
          name="fuel_price_per_liter"
          value={formData.fuel_price_per_liter}
          onChange={handleChange}
          placeholder="10000"
        />
      </div>
    </div>
  );
}

export default FuelPriceForm;
