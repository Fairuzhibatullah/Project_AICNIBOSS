import React from 'react';

function LocationForm({ formData, setFormData }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="card">
      <h2>1. Lokasi Perjalanan</h2>
      <div className="form-group">
        <label>Lokasi Asal</label>
        <input
          type="text"
          name="origin"
          value={formData.origin}
          onChange={handleChange}
          placeholder="Contoh: Stasiun Bogor"
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
        />
      </div>
    </div>
  );
}

export default LocationForm;
