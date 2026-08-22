import React from 'react';
import MapView from './MapView';
import RouteSummary from './RouteSummary';

function PredictionResult({ result }) {
  return (
    <div className="prediction-result-container">
      <div className="map-section">
        <MapView result={result} />
      </div>
      {result && (
        <div className="summary-section">
          <RouteSummary result={result} />
        </div>
      )}
    </div>
  );
}

export default PredictionResult;
