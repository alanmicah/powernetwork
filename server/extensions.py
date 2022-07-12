from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# from models import PowerStations

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/alanmicah'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'FALSE'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    

    def __repr__(self):
        return '<User %r>' % self.username

@app.route("/")
def index():
   return render_template("index.html")

if __name__=='__main__':
   app.debug=True
app.run()