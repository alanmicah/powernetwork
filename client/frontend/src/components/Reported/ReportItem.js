import './ReportItem.scss';
import Card from '../UI/Card';
import ReportDate from './ReportDate';

const ReportItem = (props) => {
  return (
    <li>
      <Card className='report-item'>
        <ReportDate date={props.date} />
        <div className='report-item__description'>
          <h2>{props.postcode}</h2>
          <div className='report-item__price'>{props.description}</div>
        </div>
      </Card>
    </li>
  );
};

export default ReportItem;
