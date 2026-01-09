import React from "react";
import { GoogleMap, LoadScript, Marker } from "@react-google-maps/api";

const containerStyle = {
  width: "100%",
  height: "100%",
};

// const center = {
//   lat: 30.601389, // Example: San Francisco
//   lng: -96.314445,
// };
const HQ_LOCATION = {
  lat: 30.627977, // latitude
  lng: -96.334407, // longitude
};

export default function MyMap({ lat, lng }) {
  return (
    <LoadScript googleMapsApiKey="AIzaSyDlBXP-eKVrXvfruf2mxNb2wlsqVUR5RKQ">
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={lat ? { lat, lng } : HQ_LOCATION}
        zoom={15}
      >
        <Marker position={{ lat, lng }} />
        <Marker
          position={HQ_LOCATION}
          label={{
            text: "HQ",
            color: "white",
            fontWeight: "bold",
          }}
          icon={{
            scale: 10,
            fillColor: "blue",
            fillOpacity: 0.8,
            strokeWeight: 1,
          }}
        />
      </GoogleMap>
    </LoadScript>
  );
}
