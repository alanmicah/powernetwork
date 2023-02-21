import { useEffect, useState, useRef } from "react";
import axios from "axios";
// import Main from './pages/Homepage';
import Reports from "./components/Reported/Reports";
import GoogleMapComponent from "./components/PloygonMap";

function App() {
  const [allReports, setAllReports] = useState([]);
  const apiKey = process.env.REACT_GOOGLE_MAPS_API;
  console.log(process.env.BACKEND_URL);

  useEffect(() => {
    axios
      .get(`${process.env.BACKEND_URL}`)
      .then((res) => {
        setAllReports(res.data ?? []);
      })
      .then((data) => console.log(data))
      .catch((e) => {
        console.error(e);
      });
  }, []);

  // useEffect(() => {
  //   fetch("http://localhost:5001")
  //     .then((res) => res.json())
  //     .then((data) => setAllReports(data));
  //   // .then((data) => console.log(data));
  // }, []);

  return (
    <div>
      <Reports items={allReports} />
      <GoogleMapComponent
        googleMapURL={
          `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=geometry,drawing,places`
          // "https://maps.googleapis.com/maps/api/js?key=AIzaSyC4R6AN7SmujjPUIGKdyao2Kqitzr1kiRg&v=3.exp&libraries=geometry,drawing,places"
        }
        loadingElement={<div style={{ height: `100%` }} />}
        containerElement={<div style={{ height: `400px` }} />}
        mapElement={<div style={{ height: `100%` }} />}
      />
    </div>
  );
}
export default App;
