"""
models.py created by Alan D 11/07/2022
"""

from extensions import db

class PowerStations(db.Model):
  """Power Stations"""
  __tablename__='power_stations'
  sitefunctionallocation = db.Column(db.VARCHAR, primary_key=True)
  licencearea = db.Column(db.Text)
  sitename = db.Column(db.Text)
  sitetype = db.Column(db.Text)
  sitevoltage = db.Column(db.Integer)
  esqcroverallrisk = db.Column(db.Text)
  gridref = db.Column(db.Text)
  siteassetcount = db.Column(db.Integer)
  electricalassetcount = db.Column(db.Integer)
  powertransformercount = db.Column(db.Integer)
  civilassetcount = db.Column(db.Integer)
  longitude = db.Column(db.Float)
  latitude = db.Column(db.Float)
  street = db.Column(db.Text)
  suburb = db.Column(db.Text)
  towncity = db.Column(db.Text)
  county = db.Column(db.Text, db.ForeignKey('flood_reports.county'))
  postcode = db.Column(db.Text)
  yearcommissioned = db.Column(db.VARCHAR)
  datecommissioned = db.Column(db.Date)
  siteclassification = db.Column(db.Text)
  assessmentdate = db.Column(db.Date)
  last_report = db.Column(db.Text)
  calculatedresistance = db.Column(db.Text)
  measuredresistance_ohm = db.Column(db.Float)
  next_assessmentdate = db.Column(db.Date)
  local_authority = db.Column(db.Text)
  local_authority_code = db.Column(db.Text)
  lastupdate = db.Column(db.TIMESTAMP)

class PowerCutReports(db.Model):
  """Power Cut Reports"""
  __tablename__='power_cut_reports'
  id = db.Column(db.Text, nullable=False, primary_key=True)
  type = db.Column(db.Text)
  postcodes = db.Column(db.Text)
  restoretime = db.Column(db.Text)
  information = db.Column(db.Text)
  starttime = db.Column(db.Text)
  reports = db.Column(db.Integer)
  lastupdate = db.Column(db.TIMESTAMP)

class FloodReports(db.Model):
  """Flood Reports"""
  __tablename__='flood_reports'
  id = db.Column(db.Text, nullable=False, primary_key=True)
  county = db.Column(db.Text, db.ForeignKey('power_stations.county'))
  description = db.Column(db.Text)
  eaAreaName = db.Column(db.Text)
  envelope = db.Column(db.VARCHAR)
  fwdCode = db.Column(db.Text)
  label = db.Column(db.Text)
  lat = db.Column(db.Float)
  long = db.Column(db.Float)
  notation = db.Column(db.Text)
  polygon = db.Column(db.Text)
  quickDialNumber = db.Column(db.Integer)
  riverOrSea = db.Column(db.Text)
  type = db.Column(db.VARCHAR)
  lastupdate = db.Column(db.TIMESTAMP)