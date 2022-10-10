import { useEffect, useState } from 'react';
import axios from 'axios';
// import Main from './pages/Homepage';
import Reports from './components/Reported/Reports';

function App() {
  const [allReports, setAllReports] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5001/')
      .then((res) => res.json())
      .then((data) => setAllReports(data));
    // .then((data) => console.log(data));
  }, []);

  return (
    <div>
      <Reports items={allReports} />
    </div>
  );
}
export default App;
