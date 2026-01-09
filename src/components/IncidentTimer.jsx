// import { useEffect, useState } from "react";

// export default function IncidentTimer({ startTime, isDispatched }) {
//   const [elapsed, setElapsed] = useState(startTime);

//   useEffect(() => {
//     if (isDispatched) return; // stop timer when dispatched

//     const interval = setInterval(() => {
//       setElapsed((prev) => prev + 1);
//     }, 1000);

//     return () => clearInterval(interval);
//   }, [isDispatched]);

//   const minutes = Math.floor(elapsed / 60);
//   const seconds = elapsed % 60;

//   return (
//     <span style={{ fontFamily: "monospace" }}>
//       {minutes}:{seconds.toString().padStart(2, "0")}
//     </span>
//   );
// }
// components/IncidentTimer.js
export default function IncidentTimer({ seconds }) {
  const m = Math.floor(seconds / 60)
    .toString()
    .padStart(2, "0");
  const s = Math.floor(seconds % 60)
    .toString()
    .padStart(2, "0");

  return (
    <span>
      {m}:{s}
    </span>
  );
}
