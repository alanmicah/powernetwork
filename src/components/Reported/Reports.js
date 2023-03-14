import { useState } from 'react';
import './Reports.scss';
import Card from '../UI/Card';
import ReportsList from './ReportsList';

function Reports(props) {
  // const allReports = props.items.filter((report) => {
  //   return report
  // });

  return (
    <Card className='reports'>
      {/* controlled custom component */}
      <ReportsList items={props.items} />
    </Card>
  );
}

export default Reports;
