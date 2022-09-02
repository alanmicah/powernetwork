"""
main.py created by Alan D 04/08/2022
"""

import json, psycopg2, sched, time, os
from flask import Flask, render_template
from models import PowerCutReports
from GetPowerCutReports import *

# Terminal Commands
# psql — PostgreSQL interactive terminal

# gc.disable()
# gc.isenabled()
# faulthandler.enable()

# event_schedule = sched.scheduler(time.time, time.sleep)
# schedule.every(1).minutes.do(func)


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)

# @app.route("/")
# def index():
#   return "Congratulations, it's a web app!"

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=8080, debug=True)


"""
Working - Connect to the local database Postgres
"""
def connect_database():
  local_connect = open('data/connect.json', 'r')
  connects = json.load(local_connect)
  # "database": "",
  # "user": "",
  # "password": "",
  # "host": "",
  # "port": ""

  try:
    #establishing the connection
    conn = psycopg2.connect(
      database=connects[0]['database'], user=connects[0]['user'], password=connects[0]['password'], host=connects[0]['host'], port= connects[0]['port']
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
    print(e)
    print('Could not connect to database')
