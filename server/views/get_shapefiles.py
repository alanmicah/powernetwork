"""
GetShapefile.py created by Alan D 09/08/2022
"""


def get_distribution_areas_shapefile():
  import requests, json

  datasetID = 'ukpn_primary_postcode_area'
  params = '?q=&facet=primary_su&facet=dno&timezone=Europe%2FLondon'
  try:
    # response = requests.get('https://ukpowernetworks.opendatasoft.com/api/v2/catalog/datasets/' + datasetID + '/records' + params, timeout=3)
    response = requests.get('https://ukpowernetworks.opendatasoft.com//api/records/1.0/search/?dataset=ukpn_primary_postcode_area&q=&facet=primary_su&facet=dno&refine.dno=LPN')
    print(str(response))
  except Exception as e:
    print('Query failed')
    print(response.status_code)
    return None

  if response.status_code == 200:
    data = response.json()

    #Write out the data to a json file  
    with open('data/distrution_shapefile.json', 'w') as f:
      json.dump(data, f)


get_distribution_areas_shapefile()