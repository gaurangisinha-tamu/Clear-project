import React from "react";
import PersonOutlineIcon from "@mui/icons-material/PersonOutline";
import LocationPinIcon from "@mui/icons-material/LocationPin";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import ErrorOutlineIcon from "@mui/icons-material/ErrorOutline";
import WhatshotIcon from "@mui/icons-material/Whatshot";
import CarCrashIcon from "@mui/icons-material/CarCrash";
import OpacityIcon from "@mui/icons-material/Opacity";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import "../styles/incidentCard.css";
import IncidentTimer from "./IncidentTimer";
import { yellow } from "@mui/material/colors";
const styles = {
  critical: { borderLeft: "15px solid red", color: "white" },
  high: { borderLeft: "15px solid #f57c00", color: "white" },
  medium: { borderLeft: "15px solid #fbc02d", color: "white" },
  low: { borderLeft: "15px solid #5285beff", color: "white" },
};

function IncidentCard({
  priority,
  name,
  location,
  time,
  injuries,
  vehicles,
  emotionScore,
  fire,
  trapped,
  onClick,
  dispatched,
  gas,
}) {
  let color = "white";
  if (emotionScore === "concerned") {
    color = "yellow";
  } else if (emotionScore === "distressed") {
    color = "orange";
  } else if (emotionScore === "panicked") {
    color = "red";
  } else if (emotionScore === "calm") {
    color = "green";
  }
  const isDispatched =
    dispatched.ambulance || dispatched.fire || dispatched.police;
  const shouldFlash = !isDispatched && time >= 75;
  return (
    <div
      onClick={onClick}
      style={{
        boxSizing: "border-box",
        width: "100%",
        padding: "16px",
        backgroundColor: "rgb(31, 41, 55)",
        height: "fit-content",
        // border: "1px solid transparent",
        borderRadius: "8px",
        display: "flex",
        flexDirection: "column",
        gap: "16px",
        ...styles[priority],
      }}
      className={`incident-${priority} ${shouldFlash ? "flash-warning" : ""}`}
    >
      <div className="name-row">
        <div className="icon-prop">
          <PersonOutlineIcon sx={{ fontSize: "34px" }} />
          <div style={{ fontSize: "24px", fontWeight: "bold" }}>
            {name} <span>({emotionScore})</span>
          </div>
        </div>
        <div className={`chip-${priority}`}>{priority}</div>
      </div>
      <div className="icon-prop">
        <LocationPinIcon sx={{ fontSize: "34px" }} />
        <div style={{ fontSize: "24px" }}>{location}</div>
      </div>
      <div className="icon-prop">
        <AccessTimeIcon sx={{ fontSize: "34px" }} />
        <div style={{ fontSize: "24px" }}>
          <IncidentTimer seconds={time} />
          {/* <IncidentTimer startTime={time} isDispatched={isDispatched} /> */}
        </div>
      </div>
      <div class="chips-container">
        {injuries && (
          <div
            style={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "center",
              alignItems: "center",
              gap: "4px",
              width: "110px",
              height: "38px",
              backgroundColor: "red",
              borderRadius: "8px",
            }}
          >
            <ErrorOutlineIcon />
            <div>Injuries</div>
          </div>
        )}
        {fire && (
          <div
            style={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "center",
              alignItems: "center",
              gap: "4px",
              width: "80px",
              height: "38px",
              backgroundColor: "#bb3d13ff",
              borderRadius: "8px",
            }}
          >
            <WhatshotIcon />
            <div>Fire</div>
          </div>
        )}
        {gas && (
          <div
            style={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "center",
              alignItems: "center",
              gap: "4px",
              width: "100px",
              height: "38px",
              backgroundColor: "#bbaa13ff",
              borderRadius: "8px",
            }}
          >
            <OpacityIcon />
            <div>Gas Leak</div>
          </div>
        )}
        {vehicles && (
          <div
            style={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "center",
              alignItems: "center",
              gap: "4px",
              width: "120px",
              height: "38px",
              backgroundColor: "#1e3a8a",
              borderRadius: "8px",
            }}
          >
            <CarCrashIcon />
            <div>{`${vehicles} vehicles`}</div>
          </div>
        )}
        {trapped && (
          <div
            style={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "center",
              alignItems: "center",
              gap: "4px",
              width: "120px",
              height: "38px",
              backgroundColor: "#581c87",
              borderRadius: "8px",
            }}
          >
            <WarningAmberIcon />
            <div>{`Trapped`}</div>
          </div>
        )}
      </div>
      <div style={{ color: "rgb(74, 222, 128)", fontSize: "22px" }}>
        <div>{dispatched.ambulance ? "✅ Ambulance Dispatched" : ""}</div>
        <div>{dispatched.fire ? "✅ Firetruck Dispatched" : ""}</div>
        <div>{dispatched.police ? "✅ Police Dispatched" : ""}</div>
      </div>
    </div>
  );
}

export default IncidentCard;
