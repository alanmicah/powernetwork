"""
PowerNetworkapi.py created by Alan D 09/06/2022
"""
import json, psycopg2, requests, urllib.request, nltk
from os import path
from urllib import response
from nltk import re, word_tokenize
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
from extensions import db
from models import PowerStations

#Terminal Commands
#psql — PostgreSQL interactive terminal

"""
Connect to the local database Postgres
"""
def connectDatabase():
  try:
    #establishing the connection
    conn = psycopg2.connect(
      database="alanmicah", user='alanmicah', password='local', host='127.0.0.1', port= '5432'
    )
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Executing an MYSQL function using the execute() method
    cursor.execute("select version()")

    #Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print("Connection established to: ",data)

    #Closing the connection
    conn.close()
  except Exception as e:
    print('Could not connect to database')

"""
Create a database table
"""
def createDatabaseTable():
  # try:
    #establishing the connection
    conn = psycopg2.connect(
      database="alanmicah", user='alanmicah', password='local', host='127.0.0.1', port= '5432'
    )
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Executing an MYSQL function using the execute() method
    cursor.execute("DROP TABLE IF EXISTS STATIONS")

    #Creating table as per requirement
    sql= '''CREATE TABLE STATIONS(
      licencearea CHAR(50) NOT NULL,
      sitename CHAR(50) NOT NULL,
      sitefunctionallocation CHAR(50) NOT NULL,
      sitetype CHAR(50) NOT NULL,
      sitevoltage INT,
      esqcroverallrisk CHAR(20),
      gridref CHAR(50) NOT NULL,
      siteassetcount INT,
      powertransformercount INT,
      electricalassetcount INT,
      civilassetcount INT,
      longitude FLOAT,
      latitude FLOAT,
      street CHAR(50) NOT NULL,
      suburb CHAR(50),
      towncity CHAR(30) NOT NULL,
      county CHAR(30) NOT NULL,
      postcode CHAR(10) NOT NULL,
      yearcommissioned DATE,
      datecommissioned DATE,
      siteclassification TEXT,
      assessmentdate DATE,
      last_report CHAR(50),
      calculatedresistance TEXT,
      measuredresistance_ohm FLOAT,
      next_assessmentdate DATE,
      local_authority CHAR(12),
      local_authority_code CHAR(9)
      )'''

    cursor.execute(sql)
    print('Table created successfully......')
    conn.commit()
    #Closing the connection
    conn.close()
  # except Exception as e:
  #   print('Table creation failed')

"""
Insert data into database table 
"""
def insertData():
  #  property = connector.get_session().query(Property).filter(Property.propid == propid ).first()
  try:
    networkTable = db.session.query(PowerStations)
  except Exception as e:
    print(e)
    print('Failed to get from PowerStations')
    return 'Failure'


"""
Retrieve data of primary sites from UK Power Networks based on a local authority.
"""
def getDataset():
  params = '/geojson?where=local_authority%3D%27Tower%20Hamlets%27&limit=-1&offset=0&timezone=Europe%2FLondon'
  datasetID = 'grid-and-primary-sites/exports'
  # datasetID = 'grid-and-primary-sites'
  # dataset = '/catalog/datasets/' + '{' + datasetID + '}'

  #Try to request from the api, if successful then attempt to retrieve data from api request
  try:
    response = requests.get('https://ukpowernetworks.opendatasoft.com/api/v2/catalog/datasets/' + datasetID + params, timeout=3)
    # response = requests.get('https://ukpowernetworks.opendatasoft.com/api/v2')
    print(str(response))
    print(response.json)
  except Exception as e:
    print('Query failed')
    print(response.status_code)
    return None

  if response.status_code != 200:
    try:
      response = requests.get('https://ukpowernetworks.opendatasoft.com/api/v2/catalog/datasets/' + datasetID + params, timeout=3)
      # response = requests.get('https://ukpowernetworks.opendatasoft.com/api/v2')
      print(str(response))
    except Exception as e:
      print('Query failed')
      print(response.status_code)
      return None

  #If the response from the request is 200 then retrieve data
  if response.status_code == 200:
    data = response.json()
    if("features" in data.keys()):
      properties={}
      features = data['features']
      # if len(features) >0:
      #   for items in features:
          # print(items['properties'])
          #For each word title() turns first letter to uppercase and all other letters to lowercase
          # print(items['properties']['sitename'].title(), items['properties']['postcode'])
    
    #Write out the data to a json file      
    with open('Powergrids.json', 'w') as f:
      json.dump(features, f)

"""
Retrieve data on Flood warnings within London.
"""
def getFloodWarnings():
  ## Try to request from the api, if successful then attempt to retrieve data from api request
  # datasetID = 'id/stations'
  # params = 'town='
  params = 'county=London'
  # params = 'E09000001'
  try:
    responseTest = requests.get('http://environment.data.gov.uk/flood-monitoring/id/floodAreas/122WAC953', timeout=3)
    # response = requests.get('http://environment.data.gov.uk/flood-monitoring/id/floodAreas/' + datasetID + params, timeout=3)
    response = requests.get('http://environment.data.gov.uk/flood-monitoring/id/floods?' + params, timeout=3)
    print(str(response))
    print(response.json)
  except Exception as e:
    print('Query failed')
    print(response.status_code)
    return None

  if responseTest.status_code == 200:
    data = responseTest.json()
    with open('Flooddata.json', 'w') as f:
      json.dump(data, f)
    if data['items']:
      print('Flood warning: \n', data['items']['county'], data['items']['description'], '\n', data['items']['riverOrSea'])
    else:
      print('No current flood warnings')

"""
Read text about relevant Live Reports from webpage. 
"""
def getLiveReports():
  try:
    response = requests.get('https://www.ukpowernetworks.co.uk/power-cut/list', timeout=3)
    print(str(response))
    print(response.json)
  except Exception as e:
    print('Query failed')
    print(response.status_code)
    return None

  if response.status_code == 200:
    data = response.json()
    print(data)

  quote_page = 'https://www.ukpowernetworks.co.uk/power-cut/list'

  ## Allows the page to be opened, viewed and read by the programm
  page = urllib.request.urlopen(quote_page)
  page_read = page.read()
  soup = BeautifulSoup(page_read, 'html.parser')

#
#----- Execute functions -----#
#
# connectDatabase()
# createDatabaseTable()
getDataset()
# getFloodWarnings()
# getLiveReports()

