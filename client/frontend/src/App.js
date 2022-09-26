import { useState } from 'react';
// import Main from './pages/Homepage';
import Reports from './components/Reported/Reports';

const All_Reports = [];

const App = () => {
  const [report, setReport] = useState(All_Reports);

  return (
    <div>
      <Reports items={report} />
    </div>
  );
};
export default App;
