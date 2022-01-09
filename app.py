# import the dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Set Up the Database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into the classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# create a flask application called "app"
app = Flask(__name__)

# Create Flask Routes

# define the welcome route
@app.route('/')

# add the routing information for each of the other routes
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Creating a new route for prepcipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
   # First, we want to add the line of code that calculates the date one year ago from the most recent date in the database. 
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   # Next, write a query to get the date and precipitation for the previous year.
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
   # Finally, we'll create a dictionary with the date as the key and the precipitation as the value.
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
   
# Creating a new route for stations
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Creating a new route for monthly temperatures
@app.route("/api/v1.0/tobs")
def temp_monthly():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
   temps = list(np.ravel(results))
   return jsonify(temps=temps)

# Creating a route for a summary statistics report
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
    


