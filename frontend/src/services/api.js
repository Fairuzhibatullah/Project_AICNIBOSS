export const predictRoute = async (formData) => {
  const url = 'http://127.0.0.1:8001/predict';
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Terjadi kesalahan saat menghubungi server.');
    }

    return data;
  } catch (error) {
    console.error("API Error:", error);
    // Kita berikan pesan error yg user friendly
    throw new Error(error.message || 'Gagal menghubungi server. Pastikan backend aktif.');
  }
};
