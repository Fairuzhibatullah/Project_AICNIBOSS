import React from 'react';

function LocationForm({ formData, setFormData }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="form-card">
      <div className="card-header">
        <span className="material-symbols-outlined">pin_drop</span>
        <h3>Lokasi Perjalanan</h3>
      </div>
      <div className="card-body">
        <div className="form-group">
          <label>Lokasi Asal</label>
          <input
            type="text"
            name="origin"
            value={formData.origin}
            onChange={handleChange}
            placeholder="Contoh: Stasiun Bogor"
            required
          />
        </div>
        <div className="form-group">
          <label>Lokasi Tujuan</label>
          <input
            type="text"
            name="destination"
            value={formData.destination}
            onChange={handleChange}
            placeholder="Contoh: Kebun Raya Bogor"
            required
          />
        </div>
      </div>
    </div>
  );
}

export default LocationForm;
