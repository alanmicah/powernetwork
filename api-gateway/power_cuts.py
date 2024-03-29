"""
power_cuts.py created by Alan D 04/08/2022

Reads, renders and parses webpage for live power cut reports.
This script should be ran as a heartbeat (executing constantly every minute or so)
"""


import json, datetime, sched, time
from extensions import db
from models import PowerCutReports
from bs4 import BeautifulSoup
from datetime import date
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

schedulerTest = sched.scheduler(time.time, time.sleep)

"""
Parse table content for power cut reports
"""
def get_reports_tbody():
    try:
        urlsJson = open('data/urls.json', 'r')
        urls = json.load(urlsJson)
        url = urls[0]["powercuts"]

        # Run Chrome in a headless/server environment. Won't open a browser window.
        options = Options()
        options.headless = True
        # options.add_argument("no-sandbox")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--disable-dev-shm-usage")

        # driver = webdriver.Chrome(service=Service('/Users/alanmicah/build/powernetwork/server/drivers/chromedriver'), options=options)
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        driver.get(url)

        # this is just to ensure that the page has the time to fully load/render.
        time.sleep(5)

        html = driver.page_source

        # this renders the JS code and stores all
        # of the information in static HTML code.

        # Applying bs4 to html variable.
        soup = BeautifulSoup(html, "html.parser")

#         # savePage = soup.contents
    except Exception as e:
        print("Failed to render webpage: " + str(e))

    try:
        # Parsing relevant elements found in the table
        textBody = soup.find("tbody")
    except Exception as e:
        print(e)
        print('Unable to find div class')

    data = []

    for row in textBody:
        ele = []
        rows = []
        for item in row:
            ele = item.text.strip()
            rows.append(ele)
        if rows:
            data.append(rows)
            
    with open('data/live_reports.json', 'w') as filehandle:
        json.dump(data, filehandle)



"""
Render and parse dynamic page content for power cut reports
"""
def get_reports():
    try:
        urlsJson = open('data/urls.json', 'r')
        urls = json.load(urlsJson)
        url = urls[0]["powercuts"]

        # Run Chrome in a headless/server environment. Won't open a browser window.
        options = Options()
        options.headless = True
        # options.add_argument("no-sandbox")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--disable-dev-shm-usage")

        # driver = webdriver.Chrome(service=Service('/Users/alanmicah/build/powernetwork/server/drivers/chromedriver'), options=options)
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        driver.get(url)

        # this is just to ensure that the page has the time to fully load/render.
        time.sleep(5)

        html = driver.page_source

        # this renders the JS code and stores all
        # of the information in static HTML code.

        # Applying bs4 to html variable.
        soup = BeautifulSoup(html, "html.parser")

        # savePage = soup.contents

    except Exception as e:
        print(e)
        print('Failed to render webpage')

    try:
        # Parsing only elements found in the table div class
        # First soup.find might not be needed
        # tableBody = soup.find(
        #     "div", {"class": "PowerCutList_PowerCutListWrapper__dy74M"})
        textBody = soup.find_all(
            "div", {"class": "PowerCutListItem_PowerCutListItem__AzYtO"})

    except Exception as e:
        print("Unable to find div class: " + str(e))

    try:
        data = []

        for row in textBody:
            cols = row.find_all('p')

            # Remove the html syntax
            cols = [ele.text.strip() for ele in cols]

            # Stores the year from the string
            check_year = cols[6].split()[-1:][0]
            #match = re.match(r'.*([1-3][0-9]{3})', l)

            # Skips report if year reported is before current year
            if check_year.isdigit():
                current_year = date.today().year
                if (int(check_year) < current_year):
                    continue

            # Not all the necessary text are found only in <p> tags
            postcodes = row.find(
                "div", class_="PowerCutListItem_PowerCutPostcodes__xlT_j")
            affected = row.find(
                "div", class_="PowerCutListItem_PowerCutCustomers__UUhFc")
            # Remove the html syntax
            postcodes = [ele.text.strip() for ele in postcodes]
            affected = [ele.text.strip() for ele in affected]

            # This element contains the amount of user reports,
            # Converts element to an int()
            if (affected[1] != '-'):
                affected[1] = int(affected[1])
            else:
                affected[1] = 0

            cols = cols + postcodes + affected

            # cols = remove_unwanted(cols)

            # Each element in 'unwanted' is used as an index of elements
            unwanted = [12, 10, 8, 7, 3, 2, 0]
            # Remove unnecessary elements at each index position found in 'unwanted'
            # for ele in unwanted:
            #     del cols[ele]
            # Implementing iter() method instead of for loop iteration
            it = iter(unwanted)
            while True:
                try:
                    x=next(it)
                except StopIteration:
                    break
                else:
                    try:
                        del cols[x]
                    except Exception as e:
                        print(e)
                        print('Unable to remove element')

            data.append(cols)
        with open('data/live_reports.json', 'w') as filehandle:
            json.dump(data, filehandle)
        print('Success')
    except Exception as e:
        print(e)



"""
Remove unnecessary elements
"""
def remove_unwanted(columns):
    # Each element represents an index
    unwanted = [12, 10, 8, 7, 3, 2, 0]
    it = iter(unwanted)
    while True:
        try:
            x=next(it)
        except StopIteration:
            break
        else:
            try:
                del columns[x]
            except Exception as e:
                print('Unable to remove element')
                return e
    return columns



"""
Upload reports to database
"""
def upload_reports():
    # Upload retrieved data in json file to database
    try:
        networkTable = db.session.query(PowerCutReports)
    except Exception as e:
        print(e)
        return 'Failure'

    reportsJson = open('data/live_reports.json', 'r')
    eachReports = json.load(reportsJson)

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
def remove_old_reports():
    try:
        networkTable = db.session.query(PowerCutReports)
    except Exception as e:
        print(e)
        print('Failed to get from PowerCutReports')
        return 'Failure'

    if networkTable is not None:
        cutoff = (datetime.datetime.now() - datetime.timedelta(days=7)
                  ).strftime('%Y-%m-%d %H:%M:%S')
        try:
            # DELTE FROM table WHERE DATE(date_time) < DATE(NOW() - INTERVAL 7 DAY)
            db.session.query(PowerCutReports).filter(
                PowerCutReports.lastupdate <= cutoff).delete()
        except Exception as e:
            print(e)
            print('Failed to query remove old reports')

        try:
            db.session.commit()
            print('Successfully removed old reports')
        except Exception as e:
            print(e)
            print('Failed to commit session')
        finally:
            db.session.close()
    else:
        return 'table is empty'


###
# -----Function calls-----#
# get_reports()
upload_reports()
# remove_old_reports()
