import { useEffect, useState } from 'react';
import axios from 'axios';
// import Main from './pages/Homepage';
import Reports from './components/Reported/Reports';

const All_Reports = [
  {
    id: 'INCD-312949-Z',
    type: 'Restored power cut',
    restoretime: 'Power was restored at: To be confirmed',
    information:
      'A fault occurred on an underground electricity cable affecting the local area.',
    starttime: 'This power cut was reported at 20:53, 30 Jun 2022',
    postcodes: 'AL6 9',
    reports: 0,
  },
  {
    id: 'INCD-288991-G',
    type: 'Restored power cut',
    restoretime: 'Power was restored at: 03 Sep 2022 between 00:30 and 01:30',
    information:
      'An underground electricity cable faulted on our high voltage network, causing an area wide power cut.',
    starttime: 'This power cut was reported at 23:08, 02 Sep 2022',
    postcodes: 'BN16 1, BN16 2, RH7 6',
    reports: 0,
  },
];

// const EachReport = (props) => {
//   return <li>{props}</li>;
// };

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
      {/* <ul>
        {allReports.map((each) => (
          <EachReport key={each.id} each={each} />
        ))}
      </ul> */}
      <Reports items={allReports} />
      {/* {allReports.map((each) => (
        <ul key={each.id}>{each.id}</ul>
      ))} */}
    </div>
  );
}
export default App;
