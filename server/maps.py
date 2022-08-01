"""
maps.py Created by Alan D 19/07/2022
"""

def get_key():
  import json

  try: 
    apikeyJson = open('data/Apikey.json', 'r')
    everyApiKey = json.load(apikeyJson)
    googlemapKey = everyApiKey[0]['googlemap']
    return googlemapKey
  except Exception as e:
    print(e)
    print('Failed to get api key')
    return None


"""
Draw the London congestion zone as a polygon with Jupyter Notebook
"""
def jupyter_gmaps():
  import gmaps

  if get_key() != None:
    gmaps.configure(api_key=get_key())

    import gmaps.datasets
    london_congestion_zone_path = gmaps.datasets.load_dataset('london_congestion_zone')
    london_congestion_zone_path[:2]
    # [(51.530318, -0.123026), (51.530078, -0.123614)]

    fig = gmaps.figure(center=(51.5, -0.01), zoom_level=12)
    london_congestion_zone_polygon = gmaps.Polygon(
      london_congestion_zone_path,
        stroke_color='blue',
        fill_color='blue'
    )
    drawing = gmaps.drawing_layer( 
      features=[london_congestion_zone_polygon],
      show_controls=False
    )
    try:
      fig.add_layer(drawing)
      fig
    except Exception as e:
      print(e)
      print('Failed to get generate map')


"""
Mapping with geopandas
"""
def geopanda_map():
  import geopandas as gpd

  boroughBoundaryMap = gpd.read_file('data/shapefiles/London_Borough_Excluding_MHW.shp')
  print("--------------------")
  print(boroughBoundaryMap.type)
  print("--------------------")
  print(boroughBoundaryMap.crs)
  print("--------------------")
  print(boroughBoundaryMap.bounds)
  print("--------------------")
  boroughBoundaryMap.plot(figsize=(5,5), edgecolor="purple", facecolor="None")


def googlemaps_maps():
  import googlemaps
  from datetime import datetime

  gmaps = googlemaps.Client(key=get_key())

  # Geocoding an address
  geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

  # Look up an address with reverse geocoding
  reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

  # Request directions via public transit
  now = datetime.now()
  directions_result = gmaps.directions("Sydney Town Hall",
                                      "Parramatta, NSW",
                                      mode="transit",
                                      departure_time=now)


"""
Execute Functions
"""
geopanda_map()