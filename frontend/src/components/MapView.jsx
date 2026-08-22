import React, { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Polyline, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix leaflet default icon issue in React
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

// Component to handle map bounds
const MapBounds = ({ bounds }) => {
  const map = useMap();
  useEffect(() => {
    if (bounds && bounds.length > 0) {
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [bounds, map]);
  return null;
};

function MapView({ result }) {
  if (!result || !result.route || !result.route.geometry) {
    return (
      <div className="map-placeholder">
        <span className="material-symbols-outlined map-placeholder-icon">map</span>
        <p>Rute akan tampil setelah perjalanan dibuat.</p>
      </div>
    );
  }

  // Transform [lon, lat] from backend to [lat, lon] for Leaflet
  const polylineCoords = result.route.geometry.map(([lon, lat]) => [lat, lon]);
  
  // Origin and destination coords for markers
  const originCoord = [result.origin.latitude, result.origin.longitude];
  const destCoord = [result.destination.latitude, result.destination.longitude];

  return (
    <div className="map-container">
      <div className="map-overlay">
        <span>{result.origin.name} &rarr; {result.destination.name}</span>
      </div>
      <MapContainer 
        center={originCoord} 
        zoom={13} 
        scrollWheelZoom={true} 
        style={{ height: '100%', width: '100%', zIndex: 1 }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {polylineCoords.length > 0 && (
          <Polyline positions={polylineCoords} color="#0e7490" weight={5} opacity={0.8} />
        )}
        
        <Marker position={originCoord} />
        <Marker position={destCoord} />
        
        <MapBounds bounds={polylineCoords} />
      </MapContainer>
    </div>
  );
}

export default MapView;
