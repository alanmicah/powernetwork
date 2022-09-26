import { useState } from 'react';
// import { createBrowserHistory } from 'history';
import Main from './pages/Homepage';
import Reports from './components/Reported/Reports';
// import ScrollToTop from './components/ScrollToTop';
// import { connect } from 'react-redux';
// import { systemActions } from './store/actions';

const NOTIFICATION_INTERVAL = 1000 * 60 * 5;

const All_Reports = [];

const App = () => {
  // useEffect(() => {
  //   const ID = setInterval(() => {
  //     if (authenticated) {
  //       fetchNotifications()
  //     }
  //   }, NOTIFICATION_INTERVAL)
  //   return () => clearInterval(ID)
  // }, [authenticated])

  const [report, setReport] = useState(All_Reports);

  return (
    <div>
      <Reports items={report} />
    </div>
  );

  // return (
  //   <div>
  //     <Router history={history}>
  //       {/* <ScrollToTop /> */}
  //       <Switch>
  //         <PrivateRoute path='/' exact component={Main} />

  //         {/* Reports */}
  //         <PrivateRoute path='/reports' exact component={IncidentReports} />
  //         <PrivateRoute path='/reports/:id' component={IncidentDetails} />

  //         {/* Locations */}
  //         <PrivateRoute path='/powergrid' exact component={PowerGrid} />
  //         <PrivateRoute path='/postcode' exact component={Postcode} />

  //         {/* Alert Action */}
  //         <PrivateRoute path='/alert-action/:id' component={AlertWorkflow} />
  //       </Switch>
  //     </Router>
  //     <FlashMessage />
  //   </div>
  // );
};

// const mapStateToProps = (state) => ({
//   authenticated: state.user.authenticated,
// });

// const mapDispatchToProps = (dispatch) => ({
//   fetchNotifications: () => dispatch(systemActions.fetchNotifications()),
// });

// export default connect(mapStateToProps, mapDispatchToProps)(App);
export default App;
