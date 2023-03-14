"""
CreateTables.py created by Alan D 04/08/2022
"""

import json, psycopg2

"""
Create a power network stations database table
"""
def create_powerstations_table():

  local_connect = open('data/connect.json', 'r')
  connects = json.load(local_connect)

  try:
    #establishing the connection
    conn = psycopg2.connect(
      database=connects[0]['database'], user=connects[0]['user'], password=connects[0]['password'], host=connects[0]['host'], port= connects[0]['port']
    )
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Executing an MYSQL function using the execute() method
    cursor.execute("DROP TABLE IF EXISTS POWER_STATIONS, POWER_STATIONS")

    #Creating table as per requirement
    commands= (
      """
      CREATE TABLE POWER_STATIONS
        (
        sitefunctionallocation VARCHAR PRIMARY KEY,
        licencearea VARCHAR,
        sitename VARCHAR,
        sitetype VARCHAR,
        sitevoltage INT,
        esqcroverallrisk VARCHAR,
        gridref VARCHAR,
        siteassetcount INT,
        powertransformercount INT,
        electricalassetcount INT,
        civilassetcount INT,
        longitude FLOAT,
        latitude FLOAT,
        street VARCHAR,
        suburb TEXT,
        towncity TEXT,
        county VARCHAR,
        postcode VARCHAR,
        yearcommissioned VARCHAR,
        datecommissioned DATE,
        siteclassification TEXT,
        assessmentdate DATE,
        last_report VARCHAR,
        calculatedresistance TEXT,
        measuredresistance_ohm FLOAT,
        next_assessmentdate DATE,
        local_authority VARCHAR,
        local_authority_code VARCHAR,
        lastupdate TIMESTAMP
        )
      """
    )

    # for command in commands:
    cursor.execute(commands)
    print('Table created successfully......')
    conn.commit()
    #Closing the connection
    conn.close()
  except Exception as e:
    print(e)
    print('Table creation failed')
    conn.close()


"""
Create a power cut reports datable table
"""
def create_powercuts_table():
  local_connect = open('data/connect.json', 'r')
  connects = json.load(local_connect)

  try:
    #establishing the connection
    conn = psycopg2.connect(
      database=connects[0]['database'], user=connects[0]['user'], password=connects[0]['password'], host=connects[0]['host'], port= connects[0]['port']
    )
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Executing an MYSQL function using the execute() method
    cursor.execute("DROP TABLE IF EXISTS POWER_CUT_REPORTS, POWER_CUT_REPORTS")

    #Creating table as per requirement
    commands= (
      """
      CREATE TABLE POWER_CUT_REPORTS
        (
        id VARCHAR PRIMARY KEY,
        type VARCHAR,
        postcodes VARCHAR,
        restoretime VARCHAR,
        information VARCHAR,
        starttime VARCHAR,
        reports INT,
        lastupdate TIMESTAMP
        )
      """
    )

    # for command in commands:
    cursor.execute(commands)
    print('Table created successfully......')
    conn.commit()
    #Closing the connection
    conn.close()
  except Exception as e:
    print(e)
    print('Table creation failed')
    conn.close()



def create_flood_report_table():
  local_connect = open('data/connect.json', 'r')
  connects = json.load(local_connect)
  try:
    #establishing the connection
    conn = psycopg2.connect(
      database=connects[0]['database'], user=connects[0]['user'], password=connects[0]['password'], host=connects[0]['host'], port= connects[0]['port']
    )
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Executing an MYSQL function using the execute() method
    cursor.execute("DROP TABLE IF EXISTS FLOOD_REPORTS, FLOOD_REPORTS")

    #Creating table as per requirement
    commands= (
      """
      CREATE TABLE FLOOD_REPORTS
        (
        id TEXT PRIMARY KEY,
        county TEXT,
        description VARCHAR,
        eaAreaName TEXT,
        envelope VARCHAR,
        fwdCode VARCHAR,
        label TEXT,
        lat FLOAT,
        long FLOAT,
        notation VARCHAR,
        polygon VARCHAR,
        quickDialNumber INT,
        riverOrSea TEXT,
        type VARCHAR,
        lastupdate TIMESTAMP
        )
      """
    )

    cursor.execute(commands)
    print('Table created successfully......')
    conn.commit()
    #Closing the connection
    conn.close()
  except Exception as e:
    print(e)
    print('Table creation failed')
    conn.close()



#----- Execute functions ------#
# create_powercuts_table()
# create_powerstations_table()