import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

const API = "http://localhost:8000";

function App() {

  const [hotspots, setHotspots] = useState([]);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    fetch(`${API}/hotspots`)
      .then(res => res.json())
      .then(data => setHotspots(data));
  }, []);

  function selectHotspot(hotspot) {
    fetch(`${API}/hotspots/${hotspot.id}`)
      .then(res => res.json())
      .then(data => setSelected(data));
  }

  return (
    <div className="app">

      <header>
        <div>
          <h1>HeatScape</h1>
          <p>Urban Heat Reduction Planner</p>
        </div>

        <span className="status">
          ● Chennai
        </span>
      </header>

      <main>

        <section className="map-section">

          <div className="map-header">
            <h2>Chennai Heat Risk</h2>

            <div className="legend">
              <span>Low</span>
              <span>Moderate</span>
              <span>High</span>
              <span>Critical</span>
            </div>
          </div>

          <MapContainer
            center={[13.0827, 80.2707]}
            zoom={11}
            className="map"
          >

            <TileLayer
              attribution="© OpenStreetMap contributors"
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {hotspots.map(h => (

              <CircleMarker
                key={h.id}
                center={[h.lat, h.lng]}
                radius={14}
                pathOptions={{
                  color: h.risk >= 75 ? "red" :
                         h.risk >= 50 ? "orange" :
                         h.risk >= 25 ? "yellow" :
                         "green"
                }}
                eventHandlers={{
                  click: () => selectHotspot(h)
                }}
              >

                <Popup>
                  <strong>Heat Risk: {h.risk}/100</strong>
                  <br />
                  LST: {h.lst}°C
                </Popup>

              </CircleMarker>

            ))}

          </MapContainer>

        </section>

        <aside>

          {!selected ? (

            <div className="empty">
              <h2>Select a hotspot</h2>
              <p>
                Click a hotspot on the map to understand
                why the area is at risk.
              </p>
            </div>

          ) : (

            <div>

              <h2>Hotspot Analysis</h2>

              <div className="risk">
                <span>Heat Risk</span>
                <strong>{selected.risk}/100</strong>
                <small>
                  {selected.risk >= 75 ? "CRITICAL" :
                   selected.risk >= 50 ? "HIGH" :
                   selected.risk >= 25 ? "MODERATE" :
                   "LOW"}
                </small>
              </div>

              <div className="stats">

                <div>
                  <span>LST</span>
                  <strong>{selected.lst}°C</strong>
                </div>

                <div>
                  <span>Built-up</span>
                  <strong>{selected.built_up}%</strong>
                </div>

                <div>
                  <span>Vegetation</span>
                  <strong>{selected.vegetation}%</strong>
                </div>

                <div>
                  <span>Population</span>
                  <strong>{selected.population}</strong>
                </div>

              </div>

              <h3>Why is this area hot?</h3>

              <p>
                High built-up intensity and low vegetation
                contribute to increased heat risk.
              </p>

              <h3>Recommended Actions</h3>

              {selected.recommendations?.map((r, i) => (

                <div className="recommendation" key={i}>
                  <strong>{r.name}</strong>
                  <p>{r.reason}</p>
                  <small>{r.priority} Priority</small>
                </div>

              ))}

            </div>

          )}

        </aside>

      </main>

    </div>
  );
}

export default App;
