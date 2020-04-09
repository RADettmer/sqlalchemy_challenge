#climate app - Randy Dettmer 4/7/2020
#import flask and set up routes
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

import datetime

#database set up
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
#reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)
#save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#create session link to the database - duplicate - already under each route - remove later
#session = Session(engine)

#flask setup
app = Flask(__name__)

# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

#flask routes
@app.route("/")
def home():
    """list all available api routes"""
    return (
        f"Welcome to the Honolulu, Hawaii Weather Analysis for Your Next Vacation!<br/>"
        f"========================================================================<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session link from python to the database
    session = Session(engine)
    """convert the query results to a dictionary using date as the key and prcp as the value"""
    #query precipitation
    results = session.query().all()

    prcp_results = list(np.rvael(results))
    return jsonify(prcp_results)
    session.close()


@app.route("/api/v1.0/stations")
def stations():
    #create session link from python to the database
    session = Session(engine)
    #return list of all station names
    results = session.query(Station.station, Station.name).all()

    sta_names = list(np.ravel(results))

    return jsonify(sta_names)
    session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    #create session link from python to the database
    session = Session(engine)
    #query stations
    tobs_results = session.query().all() #session.query(Passenger.name)  - this needs fixed
    session.close()

    #convert list of tuples into normal list
    #all_names = list(np.rvael(results))  - this needs fixed
    #return jsonify(all_names)  - this needs fixed

@app.route("/api/v1.0/<start>")
def start(start):
    #create session link from python to the database
    session = Session(engine)
    #query stations
    results = session.query().all() #session.query(Passenger.name)  - this needs fixed
    session.close()

    #convert list of tuples into normal list
    #all_names = list(np.rvael(results))  - this needs fixed
    #return jsonify(all_names)  - this needs fixed

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    #create session link from python to the database
    session = Session(engine)
    #query stations
    results = session.query().all() #session.query(Passenger.name)  - this needs fixed
    session.close()

    #convert list of tuples into normal list
    #all_names = list(np.rvael(results))  - this needs fixed
    #return jsonify(all_names)  - this needs fixed




#this needs to be present at the close of the file
if __name__=='__main__':
    app.run(debug=True)