import React from 'react';

function Home({ onStart }) {
  return (
    <div className="home-page">
      <section className="home-hero">
        <div className="home-hero-content">
          <div className="home-eyebrow">
            <span className="material-symbols-outlined">auto_awesome</span>
            AI ROUTE PREDICTOR
          </div>

          <h1>
            Perjalanan lebih cerdas,
            <br />
            konsumsi BBM lebih terukur.
          </h1>

          <p>
            BogoRoute membantu memperkirakan konsumsi BBM motor berdasarkan
            rute, kendaraan, cuaca, dan kondisi perjalanan.
          </p>

          <button className="home-cta" onClick={onStart}>
            <span className="material-symbols-outlined">route</span>
            Mulai Perjalanan
          </button>
        </div>

        <div className="home-visual">
          <div className="home-route-card">
            <div className="route-card-header">
              <span className="material-symbols-outlined">map</span>
              <span>Smart Route</span>
            </div>

            <div className="route-line">
              <div className="route-point origin"></div>
              <div className="route-path"></div>
              <div className="route-point destination"></div>
            </div>

            <div className="route-info">
              <div>
                <span>Estimasi</span>
                <strong>12.4 km/L</strong>
              </div>

              <div>
                <span>Biaya</span>
                <strong>Rp 18.500</strong>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="home-features">
        <div className="home-feature">
          <span className="material-symbols-outlined">route</span>
          <div>
            <h3>Rute</h3>
            <p>Hitung perjalanan berdasarkan rute yang dipilih.</p>
          </div>
        </div>

        <div className="home-feature">
          <span className="material-symbols-outlined">cloud</span>
          <div>
            <h3>Cuaca</h3>
            <p>Pertimbangkan kondisi cuaca dalam perjalanan.</p>
          </div>
        </div>

        <div className="home-feature">
          <span className="material-symbols-outlined">local_gas_station</span>
          <div>
            <h3>BBM</h3>
            <p>Estimasi kebutuhan dan biaya bahan bakar.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;