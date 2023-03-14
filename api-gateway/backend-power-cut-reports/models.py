from extensions import db

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