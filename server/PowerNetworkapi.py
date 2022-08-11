"""
PowerNetworkapi.py created by Alan D 09/06/2022
"""
import json, requests, datetime, faulthandler, pdb, gc, pickle, spacy, numpy
from typing import final
from os import path
from urllib import response
from extensions import db
from models import PowerStations

# gc.disable()
# gc.isenabled()
# faulthandler.enable()


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
  powergridsJson = open('data/Powergrids.json', 'r')
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
  # &county%3D%27Greater%20London%27
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
      with open('data/Powergrids.json', 'w') as f:
        json.dump(features, f)

      if len(features) >0:
        return features
      else:
        return None


#
#----- Execute functions -----#
#
# connect_database()
# create_database_table()
# add_merge_to_database()
# get_dataset()
# get_flood_warnings()

# pdb.set_trace()
