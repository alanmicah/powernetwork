import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

aoi_boundary_HARV = gpd.read_file(
  "data/shapefiles/London_Borough_Excluding_MHW.shp")
postcodes_HARV = gpd.read_file("data/CodePoint_Polygons_England/ex_sample.shp")

postcodes_HARV.plot(figsize=(20,20), edgecolor="purple", facecolor="None")