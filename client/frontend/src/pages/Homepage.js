import { useState } from 'react';

const Main = () => {
  const [viewReport, setViewReport] = useState();
  const [viewPostcode, setViewPostcode] = useState();
  const [viewGrid, setGrid] = useState();

  return (
    <Page {...controls} dark active={true}>
      {/* Header */}
      <Header onMenuOpen={openMenu} />

      {/* Search Bar */}
      <Page.Section>
        <Search />
      </Page.Section>

      <Page.Section>
        <div className='d-flex flex-column flex-gap-1'>
          <Can perform='dashboard-document-library:view'>
            <Button
              wide
              onClick={() => history.push('/documents')}
              className='mt-3'
            >
              Reports
            </Button>
          </Can>
          <Can perform='dashboard-new-incident:view'>
            <Button
              wide
              variant='warning'
              onClick={() => history.push('/actions')}
            >
              Power Grids
            </Button>
          </Can>
        </div>
      </Page.Section>

      <Can perform='dashboard-portfolio-analytics:view'>
        <div className='mt-4'>
          <MultipleHotelsCard />
        </div>
      </Can>

      <Can perform='dashboard-hotel-analytics:view'>
        <div className='mt-4'>
          {hotels?.[0] && <HotelCard hotel={hotels[0]} />}
        </div>
      </Can>

      <Can perform='dashboard-tasks:view'>
        <TasksToday />
      </Can>

      <Can perform='dashboard-summary:view'>
        <DashboardSummary />
      </Can>
    </Page>
  );
};

export default Main;
