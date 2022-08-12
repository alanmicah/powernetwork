"""
PowerCutReports.py created by Alan D 04/08/2022

Reads webapge and parses the relevant elements for the live report.
This should be ran as a heartbeat (executing constantly every minute or so)
"""
import json, datetime
from extensions import db
from models import PowerCutReports


"""
Read and parse text about relevant Live Reports from webpage.
"""
def try_live_reports():

  import requests, urllib.request
  from bs4 import BeautifulSoup

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

    # Parsing only elements found in the table
    tableBody = soup.find('table')
    wholeTable = tableBody.find('tbody')
    rows = wholeTable.find_all('tr')

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
  # cutoff = (dt.date.today() - dt.timedelta(days=DAYS)).strftime('%Y-%m-%d')
  # User.query.filter_by(date_added<=cutoff).delete()
  # db.session.commit()
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

  # DELETE FROM table WHERE date < '2011-09-21 08:21:22';



#-----Function calls-----#
# This should be called once a day
remove_old_reports()
try_live_reports()