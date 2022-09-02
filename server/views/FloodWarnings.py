"""
FloodWarnings.py created by Alan D 04/08/2022
"""

import json, requests

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
