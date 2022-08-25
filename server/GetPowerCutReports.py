"""
PowerCutReports.py created by Alan D 04/08/2022

Reads webapge and parses the relevant elements for the live report.
This script should be ran as a heartbeat (executing constantly every minute or so)
"""
import asyncio, json, requests, urllib.request, datetime, time
from extensions import db
from models import PowerCutReports
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


"""
Render and parse dynamic page content
"""
def dynamic_reports():
  try:
    url = "https://www.ukpowernetworks.co.uk/power-cut/list"
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url) 
      
    # this is just to ensure that the page is loaded
    time.sleep(5) 
      
    html = driver.page_source
    
    # this renders the JS code and stores all
    # of the information in static HTML code.

    # Now, we could simply apply bs4 to html variable
    soup = BeautifulSoup(html, "html.parser")

    savePage = soup.contents

    with open('data/ReportsRender.html', 'w', encoding='utf-8') as f:
      f.write(str(soup))

  except Exception as e:
    print(e)
    print('Failed to render webpage')


"""
Read and parse text about relevant Live Reports from webpage.
"""
"""
!!!!!!!!!! Not working !!!!!!!!!!!!
"""
def try_live_reports(): # !!! Not working !!!

  try:
    power_cut_page = 'https://www.ukpowernetworks.co.uk/power-cut/list'

    # Allows the page to be opened, viewed and read by the programm.
    page = urllib.request.urlopen(power_cut_page)
    pageRead = page.read()
    soup = BeautifulSoup(pageRead, 'html.parser')
  except Exception as e:
    print(e)
    print('Failed to open webpage')

  with requests.Session() as session:
      
    # Parsing
    response = session.get(power_cut_page)
    soup = BeautifulSoup(response.content, features='html.parser')

    try:
      # Parsing only elements found in the table
      tableBody = soup.find('table')
      wholeTable = tableBody.find('tbody')
      rows = wholeTable.find_all('tr')
      
    except Exception as e:
      print(e)
      print('Unable to find table body')

    try:
      # Extracting the first 6 <p> tags (which are the columns) in each row in the table.
      data = []
      for row in rows:
        cols = row.find_all('p')
        cols = [ele.text.strip() for ele in cols]

        # Seperate all the post codes in the string
        # cols[1] = cols[1].split(',')

        # Extract and store stripped version of each report's reference number,
        # the reference number will be used as the Primary Key in the db.
        referenceEle = cols[6].strip().split()
        cols[6] = referenceEle[0]

        # This element contains the amount of reported affected customers,
        # Converts element to an int() if it contains a value
        if (cols[5] != '-'):
          cols[5] = int(cols[5])
        else:
          cols[5] = 0
        data.append(cols[:7])

      with open('data/live_reports.json', 'w') as filehandle:
        json.dump(data, filehandle)

    except Exception as e:
      print(e)
      print('Failed to extract reports from the html table')

  try:
    networkTable = db.session.query(PowerCutReports)
  except Exception as e:
    print(e)
    print('Failed to get from PowerCutReports')
    return 'Failure'

  # features = getDataset()
  reportsJson = open('data/live_reports.json', 'r')
  eachReports = json.load(reportsJson)

  try:
    for items in eachReports:
        powercutreports = PowerCutReports()
        powercutreports.id = items[6]
        powercutreports.type = items[0]
        powercutreports.postcodes = items[1]
        powercutreports.restoretime = items[2]
        powercutreports.information = items[3]
        powercutreports.starttime = items[4]
        powercutreports.reports = items[5]
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
def remove_old_reports():
  cutoff = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
  try:
    # DELTE FROM table WHERE DATE(date_time) < DATE(NOW() - INTERVAL 7 DAY)
    db.session.query(PowerCutReports).filter(PowerCutReports.lastupdate <= cutoff).delete()
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


###
#-----Function calls-----#
# remove_old_reports()
# try_live_reports()
dynamic_reports()