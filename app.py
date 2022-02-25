import numpy as np
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.declarative import declarative_base

# import flask
from flask import Flask,jsonify

# retrieve all neccessary datas for APIs outputs
# create engine to hawaii.sqlite ~ create a virtual database itself to do further step here 

database_path = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

connect = engine.connect()
data_measurement = engine.execute("SELECT * FROM measurement")
data_station = engine.execute("SELECT * FROM station")

# View all of the classes that automap found : reflect 2 table available in DB Browser (measurement | station)

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station

# -------------------------------
# create app.py APIs routes | being sure to pass __name__

app = Flask(__name__)

## Define what to do when a user hits the index route 
# def is to define the function, and each function named must be different, 
# (tracie, cindy); if not it would be replaced

# Home page first
@app.route('/')
def index():
    return 'Home page'

# create api route for precipitation (rainfall) query
@app.route('/api/v1.0/rainfall')
def tracie():
    # create link to DB browser and query the data out
    session = Session(engine)
    Precipitation = session.query(measurement.station, measurement.prcp).all()
    session.close()
    
    precipitation = []
    for station, prcp in Precipitation:
        rain = {}
        rain["station"] = station
        rain["precipitation"] = prcp
        precipitation.append(rain)

    return jsonify(precipitation)

# create api route for station names query
@app.route('/api/v1.0/stations')
def cindy():
    # create link to DB browser and query the data out
    session = Session(engine)
    station = session.query(measurement.station).all()
    session.close()

    # Convert the data outputs above as a list of tuples into normal list 
    #  np.ravel is to convert
    
    station_list = list(np.ravel(station))
    return jsonify(station_list)

# create api route for temperature observation query
@app.route('/api/v1.0/tobs')
def phleoo():
    # create link to DB browser and query the data out
    session = Session(engine)
    temperature = session.query(measurement.station, measurement.tobs, measurement.date).all()
    session.close()

    tobs = session.query(measurement.tobs, measurement.date).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= '2016-08-23').all()

    temp = []
    for tobs, date in tobs:
        temp_obs = {}
        temp_obs["date"] = date
        temp_obs["temperature"] = tobs
        temp.append(temp_obs)

    return jsonify(temp)

@app.route('/api/v1.0/<start>')
def sean(start = None, end = None):

    # create link to DB browser and query the data out
    session = Session(engine)
    tobs = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),\
        func.max(measurement.tobs)).filter(measurement.date >= start).first()
    print(tobs)
    session.close()
    """return the temp if the date input by users are matched
       or a 404 if not."""

    #temp_per_date = start.replace(" ", "").lower()
    #if not end:
    #     #start = dt.datetime.strptime(start, "%m%d%y")

    #     # get the result if not end:
    #     result = session.query(*tobs).filter(measurement.date >= start).all()
    #     session.close()

    # for start in result:
    #     date_search = start["date"].replace(" ", "").lower()
    temp = []
    for min, avg, max in tobs:
             tobs_dict = {}
             tobs_dict['Min'] = min
             tobs_dict['Average'] = avg
             tobs_dict['Max'] = max
             temp.append(tobs_dict)

    #     #if date_search == temp_per_date:
    #         #temp = list(np.ravel(result))

    return jsonify(temp)

    #return jsonify({"error": "Character not found."}), 404


#@app.route('/api/v1.0/<start>/<end>')
#def hanah():
#    return jsonify('the avg | highest | lowest temperature from start date to end date')


if __name__ == "__main__":
    app.run(debug=True)