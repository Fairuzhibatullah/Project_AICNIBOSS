import React from 'react';

function TravelConditionForm({ formData, setFormData }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="card">
      <h2>3. Kondisi Perjalanan</h2>
      <div className="form-row">
        <div className="form-group">
          <label>Gaya Berkendara</label>
          <select name="riding_style" value={formData.riding_style} onChange={handleChange}>
            <option value="Normal">Normal</option>
            <option value="Agresif">Agresif</option>
            <option value="Santai">Santai</option>
          </select>
        </div>
        <div className="form-group">
          <label>Kecepatan Rata-rata (km/jam)</label>
          <input
            type="number"
            name="avg_speed_kmh"
            value={formData.avg_speed_kmh}
            onChange={handleChange}
            placeholder="40"
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
          />
        </div>
        <div className="form-group">
          <label>Persentase Perjalanan Dalam Kota (%)</label>
          <input
            type="number"
            name="city_percentage"
            value={formData.city_percentage}
            onChange={handleChange}
            placeholder="80"
          />
        </div>
      </div>
    </div>
  );
}

export default TravelConditionForm;
