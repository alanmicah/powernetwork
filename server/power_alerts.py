"""
power_alert.py created by Alan D 16/08/2022

Searches for the power grid sub station postcode in the live reports database.
If it's in the database then the latest report will be returned.
"""
from flask import Flask
from extensions import db
from models import PowerCutReports, PowerStations

def match_stations_reports():

  try:
    tableStations = db.session.query(PowerStations)
  except Exception as e:
    print(e)
    print('Failed to query PowerStations table')

  try:
    tableReports = db.session.query(PowerCutReports)
  except Exception as e:
    print(e)
    print('Failed to query PowerCutReports table')

  if (tableReports and tableStations is not None):
    matching = db.session.query(PowerStations, PowerCutReports).filter(PowerCutReports.postcodes.like(PowerStations.postcode))

  # powerstations = PowerStations()
  # postcodeStation = powerstations.postcode
  # print(postcodeStation)

async def fetch_stations_reports():
  try:
    tableStations = db.session.query(PowerStations)
  except Exception as e:
    print(e)
    print('Failed to query PowerStations table')

  try:
    tableReports = db.session.query(PowerCutReports)
  except Exception as e:
    print(e)
    print('Failed to query PowerCutReports table')
  
  if (tableReports and tableStations is not None):
    await()
  print("async")
  

match_stations_reports()