"""
PowerNetworkapi.py created by Alan D 09/06/2022
"""
import json, psycopg2, requests, urllib.request, nltk, datetime
from typing import final
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
Working - Connect to the local database Postgres
"""
def connect_database():
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
def create_database_table():
  try:
    #establishing the connection
    conn = psycopg2.connect(
      database="alanmicah", user='alanmicah', password='local', host='127.0.0.1', port= '5432'
    )
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Executing an MYSQL function using the execute() method
    cursor.execute("DROP TABLE IF EXISTS STATIONS, FLOOD_REPORTS")

    #Creating table as per requirement
    commands= (
      """
      CREATE TABLE STATIONS
        (
        sitefunctionallocation VARCHAR PRIMARY KEY,
        licencearea VARCHAR,
        sitename VARCHAR,
        sitetype VARCHAR,
        sitevoltage INT,
        esqcroverallrisk VARCHAR,
        gridref VARCHAR,
        siteassetcount INT,
        powertransformercount INT,
        electricalassetcount INT,
        civilassetcount INT,
        longitude FLOAT,
        latitude FLOAT,
        street VARCHAR,
        suburb TEXT,
        towncity TEXT,
        county VARCHAR,
        postcode VARCHAR,
        yearcommissioned INT,
        datecommissioned DATE,
        siteclassification TEXT,
        assessmentdate DATE,
        last_report VARCHAR,
        calculatedresistance TEXT,
        measuredresistance_ohm FLOAT,
        next_assessmentdate DATE,
        local_authority VARCHAR,
        local_authority_code VARCHAR,
        lastupdate TIMESTAMP
        )
      """,
      """
      CREATE TABLE FLOOD_REPORTS
        (
        id TEXT PRIMARY KEY,
        county TEXT,
        description VARCHAR,
        eaAreaName TEXT,
        envelope VARCHAR,
        fwdCode VARCHAR,
        label TEXT,
        lat FLOAT,
        long FLOAT,
        notation VARCHAR,
        polygon VARCHAR,
        quickDialNumber INT,
        riverOrSea TEXT,
        type VARCHAR,
        lastupdate TIMESTAMP
        )
      """
    )

    for command in commands:
      cursor.execute(command)
    print('Table created successfully......')
    conn.commit()
      #Closing the connection
    conn.close()
  except Exception as e:
    print(e)
    print('Table creation failed')
    conn.close()


"""
Insert data into database table 
"""
def add_merge_to_database():
  #  property = connector.get_session().query(Property).filter(Property.propid == propid ).first()
  try:
    networkTable = db.session.query(PowerStations)
  except Exception as e:
    print(e)
    print('Failed to get from PowerStations')
    return 'Failure'

  # features = getDataset()
  powergridsJson = open('Powergrids.json', 'r')
  features = json.load(powergridsJson)
  
  for items in features:
    try:
      powerstations = PowerStations()
      powerstations.sitefunctionallocation = items['properties']['sitefunctionallocation']
      powerstations.licencearea = items['properties']['licencearea']
      powerstations.sitename = items['properties']['sitename']
      powerstations.sitetype = items['properties']['sitetype']
      powerstations.sitevoltage = items['properties']['sitevoltage']
      powerstations.esqcroverallrisk = items['properties']['esqcroverallrisk']
      powerstations.gridref = items['properties']['gridref']
      powerstations.siteassetcount = items['properties']['siteassetcount']
      powerstations.powertransformercount = items['properties']['powertransformercount']
      powerstations.electricalassetcount = items['properties']['electricalassetcount']
      powerstations.civilassetcount = items['properties']['civilassetcount']
      powerstations.longitude = items['properties']['longitude']
      powerstations.latitude = items['properties']['latitude']
      powerstations.street = items['properties']['street']
      powerstations.suburb = items['properties']['suburb']
      powerstations.towncity = items['properties']['towncity']
      powerstations.county = items['properties']['county']
      powerstations.postcode = items['properties']['postcode']
      powerstations.yearcommissioned = items['properties']['yearcommissioned']
      powerstations.datecommissioned = items['properties']['datecommissioned']
      powerstations.siteclassification = items['properties']['siteclassification']
      powerstations.assessmentdate = items['properties']['assessmentdate']
      powerstations.last_report = items['properties']['last_report']
      powerstations.calculatedresistance = items['properties']['calculatedresistance']
      powerstations.measuredresistance_ohm = items['properties']['measuredresistance_ohm']
      powerstations.next_assessmentdate = items['properties']['next_assessmentdate']
      powerstations.local_authority = items['properties']['local_authority']
      powerstations.local_authority_code = items['properties']['local_authority_code']
      powerstations.lastupdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

      if networkTable is not None:
        db.session.merge(powerstations)
      else:
        db.session.add(powerstations)

    except Exception as e:
      db.session.rollback()
      print(e)
      print('Failed to upload Power Station Data')
  
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
Retrieve data of primary sites from UK Power Networks based on a local authority.
"""
def get_dataset():
  params = '/geojson?where=local_authority%3D%27Tower%20Hamlets%27&limit=-1&offset=0&timezone=Europe%2FLondon'
  datasetID = 'grid-and-primary-sites/exports'

  #Try to request from the api, if successful then attempt to retrieve data from api request
  try:
    response = requests.get('https://ukpowernetworks.opendatasoft.com/api/v2/catalog/datasets/' + datasetID + params, timeout=3)
    # response = requests.get('https://ukpowernetworks.opendatasoft.com/api/v2')
    print(str(response))
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
      features = data['features']

      #Write out the data to a json file  
      with open('Powergrids.json', 'w') as f:
        json.dump(features, f)

      if len(features) >0:
        return features
      else:
        return None


"""
Retrieve data on Flood warnings within London.
"""
def get_flood_warnings():
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
def get_live_reports():
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
# connect_database()
# create_database_table()
add_merge_to_database()
# get_dataset()
# get_flood_warnings()
# get_live_reports()

