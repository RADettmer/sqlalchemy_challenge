#climate app - Randy Dettmer 4/7/2020
#import flask and set up routes
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as numpy

#database set up
engine = create_engine("sqlite:///hawaii.sqlite")
#reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)
#save reference to the table
#Passenger = Base.classes.passenger ---- not the correct file name here - needs fixed

#flask setup
app = Flask(__name__)

#flask routes
@app.route("/")
def home():
    """list all available api routes"""
    return (
        f"Welcome to the Honolulu, Hawaii Weather Analysis for Your Next Vacation!"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("api/v1.0/precipitation")
def precipitation():
    #create session link from python to the database
    session = Session(engine)
    """convert the query results to a dictionary using date as the key and prcp as the value"""
    #query precipitation
    results = session.query().all() #session.query(Passenger.name)  - this needs fixed
    session.close()

    #convert list of tuples into normal list
    #all_names = list(np.rvael(results))  - this needs fixed
    #return jsonify(all_names)  - this needs fixed

@app.route("api/v1.0/stations")
def stations():
    #create session link from python to the database
    session = Session(engine)
    #query stations
    results = session.query().all() #session.query(Passenger.name)  - this needs fixed
    session.close()

    #convert list of tuples into normal list
    #all_names = list(np.rvael(results))  - this needs fixed
    #return jsonify(all_names)  - this needs fixed

@app.route("api/v1.0/tobs")
def tobs():
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