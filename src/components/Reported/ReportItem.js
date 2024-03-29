import './ReportItem.scss';
import Card from '../UI/Card';
// import ReportDate from './ReportDate';

const ReportItem = (props) => {
  return (
    <li>
      <Card className='report-item'>
        {/* <ReportDate date={props.date} /> */}
        <div className='report-item__description'>
          <h2>{props.starttime}</h2>
          <h2>{props.postcodes}</h2>
          <div className='report-item__price'>{props.type}</div>
          <h3>{props.restore}</h3>
        </div>
      </Card>
    </li>
  );
};

export default ReportItem;
