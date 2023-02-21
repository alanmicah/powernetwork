import asyncio, os, json, datetime, re, time
from datetime import date

from extensions import db
from models import PowerCutReports

from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner
from prefect.blocks.system import JSON

import power_cuts

# Terminal command: prefect orion start

"""
Render and parse dynamic page content for power cut reports
"""
@task(retries=3)
def render_reports():
  from bs4 import BeautifulSoup
  from selenium import webdriver
  from selenium.webdriver.chrome.service import Service
  from selenium.webdriver.chrome.options import Options
  from webdriver_manager.chrome import ChromeDriverManager

  try:
    url = "https://www.ukpowernetworks.co.uk/power-cut/list"

    # Run Chrome in a headless/server environment. Won't open a browser window.
    options = Options()
    options.headless = True
    # Uncomment options if needed to run on your machine
    # options.add_argument("no-sandbox")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--disable-dev-shm-usage")

    # [1]
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get(url) 
    
    # this is just to ensure that the page is loaded.
    time.sleep(5)
  
    html = driver.page_source
    
    # this renders the JS code and stores all
    # of the information in static HTML code.

    # Applying bs4 to html variable.
    soup = BeautifulSoup(html, "html.parser")

    # savePage = soup.contents
    return soup

  except Exception as e:
    print('Failed to render webpage')
    print(e)
    return None



@task(description="This task renders and data scrapes webpage")
def get_reports():
  soup = render_reports.fn()
  try:
    # Parsing only elements found in the table div class
    # tableBody = soup.find("div", {"class": "PowerCutList_PowerCutListWrapper__dy74M"})
    textBody = soup.find_all("div", {"class": "PowerCutListItem_PowerCutListItem__AzYtO"})
    
  except Exception as e:
    print(e)
    print('Unable to find div class')

  try:
    data = []

    for row in textBody:
      cols = row.find_all('p')
      #postcodes = row.find("div", {"class": "PowerCutListItem_PowerCutPostcodes__xlT_j"})
      cols = [ele.text.strip() for ele in cols]

      # skips report if year is earlier than current year
      check_year = cols[6].split()[-1:][0]

      if check_year.isdigit():
        # match = re.match(r'.*([1-3][0-9]{3})', l)  
        current_year = date.today().year
        if(int(check_year) < current_year):
          continue

      # Not all the necessary text are found only in <p> tags
      # Would it be better seperate these lines of code?
      # postcodes = row.find("div", class_="PowerCutListItem_PowerCutPostcodes__xlT_j")
      affected = row.find("div", class_="PowerCutListItem_PowerCutCustomers__UUhFc")
      # Strip postcodes and amount of customer reports
      cols += [ele.text.strip() for ele in row.find("div", class_="PowerCutListItem_PowerCutPostcodes__xlT_j")]
      affected = [ele.text.strip() for ele in affected]

      # This element contains the amount of reported affected customers,
      # Converts element to type int
      if affected[1].isdigit():
        affected[1] = int(affected[1])
      else:
        affected[1] = 0
      cols += affected
      
      # Each element in 'unwanted' is used as an index of elements
      unwanted = [0,2,3,7,8,10,12]
      # Remove unnecessary elements at each index position found in 'unwanted'
      for ele in sorted(unwanted, reverse = True):
        del cols[ele]
      
      data.append(cols)

    with open('data/live_reports.json', 'w') as filehandle:
      json.dump(data, filehandle)
        
  except Exception as e:
    print(e)
    print('Unable to extract <p> columns')



@task(description="This task uploads reports to database")
def upload_reports():
  # Upload retrieved data in json file to database
  try:
    networkTable = db.session.query(PowerCutReports)
  except Exception as e:
    print(e)
    print('Failed to get from PowerCutReports')
    return 'Failure'
  
  reportsJson = open('data/live_reports.json', 'r') 
  eachReports = json.load(reportsJson)

  # json_block = JSON.load("power_reports")
  # print(json_block.value([1]))

  try:
    for items in eachReports:
        powercutreports = PowerCutReports()
        powercutreports.id = items[4]
        powercutreports.type = items[0]
        powercutreports.postcodes = items[5]
        powercutreports.restoretime = items[1]
        powercutreports.information = items[2]
        powercutreports.starttime = items[3]
        powercutreports.reports = items[6]
        powercutreports.lastupdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if networkTable is not None:
          db.session.merge(powercutreports)
        else:
          db.session.add(powercutreports)

  except Exception as e:
    db.session.rollback()
    print(e)
    print('Failed to upload Power Cut Reports')
  
  try:
    db.session.commit()
    print('Success')
    return 'Success'
  except Exception as e:
    db.session.rollback()
    print(e)
    print('Failed to upload')
    return str(e)
  finally:
    db.session.close()



"""
Delete rows from before a certain date
"""
@task(description="This task removes reports past a certain date")
def remove_old_reports():
  cutoff = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
  # powerType = "Restored power cut"
  try:
    # DELTE FROM table WHERE DATE(date_time) < DATE(NOW() - INTERVAL 7 DAY)
    db.session.query(PowerCutReports).filter(PowerCutReports.lastupdate <= cutoff).delete()
    # ((PowerCutReports.lastupdate <= cutoff) & (PowerCutReports.type == powerType)) | (PowerCutReports.lastupdate <= cutoff)
  except Exception as e:
    print(e)
    print('Failed to query remove old reports')

  try:  
    db.session.commit()
    print('Success')
  except Exception as e:
    print(e)
    print('Failed to commit session')
  finally:
    db.session.close()


"""
flow
"""
@flow(name="update reports",
      # task_runner=SequentialTaskRunner(),
      description="Render and parse dynamic page content for power cut reports, and also remove old reports",
      version=os.getenv("GIT_COMMIT_SHA"))
def update_reports():
  # soup = render_reports().sumbit()
  # get_reports.submit(soup)
  # upload_reports.submit()
  # render_reports()
  get_reports()
  upload_reports()
  # remove_old_reports.submit()


if __name__ == "__main__":
  # run the flow!
  update_reports()