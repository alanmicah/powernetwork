import ReportItem from './ReportItem';
import './ReportsList.scss';

function ReportsList(props) {
  if (props.items.length === 0) {
    return <h2 className='reports-list__fallback'>Found no reports</h2>;
  }

  return (
    <ul className='reports-list'>
      {props.items.map((report) => (
        <ReportItem
          key={report.id}
          type={report.type}
          postcodes={report.postcodes}
          restore={report.restoretime}
        />
      ))}
    </ul>
  );
}

export default ReportsList;
