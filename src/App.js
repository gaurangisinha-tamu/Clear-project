import IncidentCard from "./components/IncidentCard";
import "./styles/App.css";
import React from "react";
import { useState, useEffect } from "react";
import ErrorOutlineIcon from "@mui/icons-material/ErrorOutline";
import { incidents as initialIncidents } from "./incidents";
import LocalPhoneOutlinedIcon from "@mui/icons-material/LocalPhoneOutlined";
import LocationPinIcon from "@mui/icons-material/LocationPin";
import NearMeOutlinedIcon from "@mui/icons-material/NearMeOutlined";
import Button from "@mui/material/Button";
import MyMap from "./components/MyMap";
import IncidentTimer from "./components/IncidentTimer";

function App() {
  const [incidents, setIncidents] = useState(initialIncidents);
  const [ambulances, setAmbulances] = useState(8);
  const [fireTrucks, setFireTrucks] = useState(5);
  const [police, setPolice] = useState(15);

  const GOAL_TIME = 75;
  function updateIncidentFromBackend(incidentId, data) {
    setIncidents((prev) =>
      prev.map((incident) =>
        incident.id === incidentId
          ? {
              ...incident,
              injuries: data.facts.people_injured,
              fire: data.facts.has_fire,
              vehicles: data.facts.num_vehicles,
              trapped: data.facts.is_trapped,
              gas: data.facts.has_fuel_leak,
              priority: data.triage_label,
              generatedResponse: data.generated_response,
              transcript: data.transcript,
              ready: true,
              time: 0,
              createdAt: 0,
              emotionScore: data.emotion_class,
            }
          : incident
      )
    );
  }
  const avgDispatchTimeSec = React.useMemo(() => {
    const completed = incidents.filter((i) => i.dispatchedAt);

    if (completed.length === 0) return 0;

    const totalMs = completed.reduce(
      (sum, i) => sum + (i.dispatchedAt - i.createdAt),
      0
    );

    return totalMs / completed.length;
  }, [incidents]);

  // ------------------------------
  // RUN AUDIO PROCESSING SEQUENTIALLY
  // ------------------------------
  useEffect(() => {
    fetch("http://localhost:5000/incident/1/transcribe")
      .then((res) => res.json())
      .then((data) => updateIncidentFromBackend(1, data));

    // After 30 seconds → process Incident 2
    const t1 = setTimeout(() => {
      fetch("http://localhost:5000/incident/2/transcribe")
        .then((res) => res.json())
        .then((data) => updateIncidentFromBackend(2, data));
    }, 50000);

    // After 60 seconds → process Incident 3
    const t2 = setTimeout(() => {
      fetch("http://localhost:5000/incident/3/transcribe")
        .then((res) => res.json())
        .then((data) => updateIncidentFromBackend(3, data));
    }, 70000);

    const t3 = setTimeout(() => {
      fetch("http://localhost:5000/incident/4/transcribe")
        .then((res) => res.json())
        .then((data) => updateIncidentFromBackend(4, data));
    }, 90000);
    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
    };
  }, []);

  // ------------------------------
  // TIMER: UPDATES EVERY SECOND
  // ------------------------------
  const [selectedIncident, setSelectedIncident] = useState(null);

  useEffect(() => {
    const interval = setInterval(() => {
      setIncidents((prev) => {
        const updated = prev.map((inc) => {
          const hasUnits =
            inc.dispatched.ambulance ||
            inc.dispatched.fire ||
            inc.dispatched.police;

          // If units were dispatched for the FIRST time:
          if (hasUnits && !inc.dispatchedAt) {
            return {
              ...inc,
              dispatchedAt: inc.time,
            };
          }

          // If NOT dispatched yet, increment incident timer
          if (!hasUnits) {
            return {
              ...inc,
              time: inc.time + 1,
            };
          }

          // Already dispatched, unchanged
          return inc;
        });

        // Sync selected incident with updated list
        setSelectedIncident((prevSel) => {
          if (!prevSel) return prevSel;
          return updated.find((i) => i.id === prevSel.id) || prevSel;
        });

        return updated;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  // ------------------------------
  // SELECT INCIDENT
  // ------------------------------
  const handleCardClick = (incident) => {
    setSelectedIncident(incident);
  };

  // ------------------------------
  // DISPATCH UNIT
  // ------------------------------
  const handleDispatch = (id, unitType) => {
    setIncidents((prev) =>
      prev.map((inc) =>
        inc.id === id
          ? {
              ...inc,
              dispatched: { ...inc.dispatched, [unitType]: true },
            }
          : inc
      )
    );

    setSelectedIncident((prev) =>
      prev?.id === id
        ? {
            ...prev,
            dispatched: { ...prev.dispatched, [unitType]: true },
          }
        : prev
    );
  };

  return (
    <div className="app-container">
      <div className="column-container">
        {/* ACTIVE INCIDENTS LIST */}
        <div className="active-incidents-column">
          <div className="active-incidents-header">
            <div className="ai-title">
              <ErrorOutlineIcon
                sx={{ fontSize: "46px", margin: 0, padding: 0, color: "red" }}
              />
              <div>Active Incidents</div>
            </div>
            <div className="active-calls">{incidents.length} active calls</div>
          </div>

          <div className="incidents-container">
            {incidents
              .slice()
              .sort((a, b) => {
                const aDispatched =
                  a.dispatched.ambulance ||
                  a.dispatched.fire ||
                  a.dispatched.police;
                const bDispatched =
                  b.dispatched.ambulance ||
                  b.dispatched.fire ||
                  b.dispatched.police;

                if (aDispatched !== bDispatched) {
                  return aDispatched ? 1 : -1;
                }

                const priorityOrder = {
                  critical: 1,
                  high: 2,
                  medium: 3,
                  low: 4,
                };

                if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
                  return priorityOrder[a.priority] - priorityOrder[b.priority];
                }

                return b.time - a.time;
              })
              .filter((i) => i.ready)
              .map((incident) => (
                <IncidentCard
                  key={incident.id}
                  {...incident}
                  onClick={() => handleCardClick(incident)}
                />
              ))}
          </div>
        </div>

        {/* CURRENT INCIDENT DETAILS */}
        <div className="current-incident-column">
          {selectedIncident ? (
            <>
              <div className="current-header">
                <div className="current-name-row">
                  <div className="current-name">{selectedIncident.name}</div>
                  <div
                    className={`chip-${selectedIncident.priority}`}
                    style={{ width: "150px", height: "55px" }}
                  >
                    {selectedIncident.priority}
                  </div>
                </div>

                <div className="phone-row">
                  <LocalPhoneOutlinedIcon sx={{ fontSize: "32px" }} />
                  <div>{selectedIncident.phone}</div>
                </div>
              </div>

              <div className="middle-scroll">
                {/* LOCATION */}
                <div className="location-group">
                  <div className="sub-header">
                    <LocationPinIcon sx={{ fontSize: "30px" }} />
                    <div>Location</div>
                  </div>
                  <div className="location">{selectedIncident.location}</div>
                  <div className="map">
                    <MyMap
                      lat={selectedIncident.latitude}
                      lng={selectedIncident.longitude}
                    />
                  </div>
                </div>

                {/* DETAILS */}
                <div className="incident-details">
                  <div className="sub-header">
                    <ErrorOutlineIcon sx={{ fontSize: "30px" }} />
                    <div>Incident Details</div>
                  </div>

                  <div className="incident-sub-container">
                    <div className="incident-right">
                      <div className="incident-group">
                        <div style={{ color: "rgb(156, 163, 175)" }}>
                          Time Elapsed
                        </div>
                        <div style={{ fontWeight: "bold" }}>
                          <IncidentTimer seconds={selectedIncident.time} />
                        </div>
                      </div>

                      <div className="incident-group">
                        <div style={{ color: "rgb(156, 163, 175)" }}>
                          Injuries
                        </div>
                        <div style={{ fontWeight: "bold" }}>
                          {selectedIncident.injuries ? "Yes" : "No"}
                        </div>
                      </div>

                      <div className="incident-group">
                        <div style={{ color: "rgb(156, 163, 175)" }}>
                          Entrapment
                        </div>
                        <div style={{ fontWeight: "bold" }}>
                          {selectedIncident.trapped ? "Yes" : "No"}
                        </div>
                      </div>
                    </div>

                    <div className="incident-right">
                      <div className="incident-group">
                        <div style={{ color: "rgb(156, 163, 175)" }}>
                          Vehicles
                        </div>
                        <div style={{ fontWeight: "bold" }}>
                          {selectedIncident.vehicles || "None"}
                        </div>
                      </div>

                      <div className="incident-group">
                        <div style={{ color: "rgb(156, 163, 175)" }}>Fire</div>
                        <div style={{ fontWeight: "bold" }}>
                          {selectedIncident.fire ? "Yes" : "No"}
                        </div>
                      </div>

                      <div className="incident-group">
                        <div style={{ color: "rgb(156, 163, 175)" }}>
                          Units Dispatched?
                        </div>
                        <div style={{ fontWeight: "bold" }}>
                          {selectedIncident.dispatched.ambulance ||
                          selectedIncident.dispatched.fire ||
                          selectedIncident.dispatched.police
                            ? "Yes"
                            : "No"}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* VOICE TRANSCRIPT */}
                <div className="voice-container">
                  <div
                    style={{
                      fontSize: "30px",
                      fontWeight: "bold",
                      color: "white",
                    }}
                  >
                    Voice Transcript
                  </div>
                  <div className="transcript-box">
                    {selectedIncident.transcript}
                  </div>
                  <div
                    style={{ fontSize: "22px", color: "rgb(107, 114, 128)" }}
                  >
                    Live transcription from caller
                  </div>
                </div>

                {/* AI SUGGESTIONS */}
                <div className="voice-container">
                  <div
                    style={{
                      fontSize: "30px",
                      fontWeight: "bold",
                      color: "white",
                    }}
                  >
                    AI Suggestions
                  </div>
                  <div className="transcript-box">
                    {selectedIncident.generatedResponse}
                  </div>
                  <div
                    style={{
                      fontSize: "30px",
                      fontWeight: "bold",
                      color: "white",
                    }}
                  >
                    Recommended Dispatch Units
                  </div>
                  <div className="transcript-box">
                    Police{" "}
                    {(selectedIncident.fire || selectedIncident.gas) && (
                      <>, Fire Department</>
                    )}
                    {selectedIncident.injuries && <>, Ambulance</>}
                  </div>
                  <div
                    style={{ fontSize: "22px", color: "rgb(107, 114, 128)" }}
                  >
                    Suggestions from ChatGPT
                  </div>
                </div>

                {/* DISPATCH BUTTONS */}
                <div className="dispatch-units-container">
                  <div className="sub-header">
                    <NearMeOutlinedIcon sx={{ fontSize: "30px" }} />
                    <div>Dispatch Units</div>
                  </div>

                  <div className="dispatch-buttons">
                    <Button
                      onClick={() => {
                        handleDispatch(selectedIncident.id, "ambulance");
                        setAmbulances((prev) => prev - 1);
                      }}
                      variant="contained"
                      sx={{
                        width: "200px",
                        height: "75px",
                        fontSize: "28px",
                        borderRadius: "16px",
                        textTransform: "capitalize",
                        backgroundColor: "red",
                      }}
                    >
                      Ambulance
                    </Button>

                    <Button
                      onClick={() => {
                        handleDispatch(selectedIncident.id, "fire");
                        setFireTrucks((prev) => prev - 1);
                      }}
                      variant="contained"
                      sx={{
                        width: "200px",
                        height: "75px",
                        fontSize: "28px",
                        borderRadius: "16px",
                        textTransform: "capitalize",
                        backgroundColor: "#da4500ff",
                      }}
                    >
                      Fire
                    </Button>

                    <Button
                      onClick={() => {
                        handleDispatch(selectedIncident.id, "police");
                        setPolice((prev) => prev - 1);
                      }}
                      variant="contained"
                      sx={{
                        width: "200px",
                        height: "75px",
                        fontSize: "28px",
                        borderRadius: "16px",
                        textTransform: "capitalize",
                      }}
                    >
                      Police
                    </Button>
                  </div>
                </div>

                {/* NOTES */}
                <div className="dispatcher-notes">
                  <div style={{ fontWeight: "bold", fontSize: "30px" }}>
                    Dispatcher Notes
                  </div>
                  <textarea placeholder="Add notes about the incident..." />
                </div>
              </div>
            </>
          ) : (
            <div style={{ padding: 40, color: "gray" }}>
              Select an incident to view details.
            </div>
          )}
        </div>

        {/* RIGHT COLUMN */}
        <div className="right-column">
          <h1>Additional Information</h1>
          <div
            style={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "space-between",
            }}
          >
            <div
              style={{ display: "flex", flexDirection: "column", gap: "15px" }}
            >
              <div class="sh">Average Time</div>
              <div className="avg-time">
                {/* {totalDispatched === 0
                  ? 0
                  : totalDispatchTime / totalDispatched} */}
                {/* {avgDispatchTimeSec.toFixed(3)}s */}
                <div
                  style={{ fontWeight: "bold" }}
                  className={
                    avgDispatchTimeSec > GOAL_TIME ? "danger" : "avg-time"
                  }
                >
                  <IncidentTimer seconds={avgDispatchTimeSec} />
                </div>
              </div>
            </div>
            <div
              style={{ display: "flex", flexDirection: "column", gap: "15px" }}
            >
              <div class="sh">Goal Time</div>
              <div className="avg-time">1:10</div>
            </div>
          </div>
          <div className="section-header">
            <div className="sh">Available Units</div>

            <div className="units-row">
              <div className="lg">Ambulances</div>
              <div className="gr">{ambulances} available</div>
            </div>

            <div className="units-row">
              <div className="lg">Fire Trucks</div>
              <div className="gr">{fireTrucks} available</div>
            </div>

            <div className="units-row">
              <div className="lg">Police Units</div>
              <div className="gr">{police} available</div>
            </div>
          </div>

          <div className="section-header">
            <div className="sh">Severity Legend</div>

            <div className="legend-row">
              <div className="square rd"></div>
              <div>Critical - Immediate response</div>
            </div>

            <div className="legend-row">
              <div className="square or"></div>
              <div>High - Urgent response</div>
            </div>

            <div className="legend-row">
              <div className="square mo"></div>
              <div>Medium - Standard response</div>
            </div>

            <div className="legend-row">
              <div className="square lb"></div>
              <div>Low - Minor incident</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
