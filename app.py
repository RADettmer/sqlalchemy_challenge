#climate app - Randy Dettmer 4/7/2020
#import flask and set up routes
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import numpy as np

import datetime as dt

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
session = Session(engine)

#create end of search query - final date
f_date = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
max_date_str = f_date[0][0]
max_date = dt.datetime.strptime(max_date_str, "%Y-%m-%d")
#create beginning of search query - start date
s_date = max_date - dt.timedelta(365)

#flask setup
app = Flask(__name__)

#flask routes
@app.route("/")
@app.route("/home")
def home():
    """list all available api routes"""
    return (
        f"Welcome to the Honolulu, Hawaii Weather Analysis for Your Next Vacation!<br/>"
        f"========================================================================<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/Precipitation<br/>"
        f"/api/v1.0/Stations<br/>"
        f"/api/v1.0/TOBS<br/>"
        f"/api/v1.0/datesearch/2016-08-23<br/>"
        f"/api/v1.0/rangesearch/2016-10-14/2017-11-14"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session link from python to the database
    session = Session(engine)
    """Convert the query results to a dictionary using date as the key and prcp as the value"""
    
    #create begining date and ending date variables 
    #create end of search query - final date
    f_date = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    max_date_str = f_date[0][0]
    max_date = dt.datetime.strptime(max_date_str, "%Y-%m-%d")
    #create beginning of search query - start date
    s_date = max_date - dt.timedelta(365)

    """Return dates and precipitiation amounts for specific date range"""
    #query all precipitation amounts for specific date range
    results1 = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= s_date).all()
        
    #create a dictionary with the date as the key and the prcp value as the value
    all_prcp = []
    for date, prcp in results1:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)
    
    session.close()
    
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    #create session link from python to the database
    session = Session(engine)
    
    """Return a list of all station names"""
    #query all station names
    results2 = session.query(Station.station, Station.name).all()

    #convert list of tuples into a normal list
    sta_names = list(np.ravel(results2))
    
    session.close()

    return jsonify(sta_names)

@app.route("/api/v1.0/tobs")
def tobs():
    #create session link from python to the database
    session = Session(engine)

    #create begining date and endinging date variables 
    #create end of search query - final date
    f_date = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    max_date_str = f_date[0][0]
    max_date = dt.datetime.strptime(max_date_str, "%Y-%m-%d")
    #create beginning of search query - start date
    s_date = max_date - dt.timedelta(365)

    #query tobs for last year of data for most active station
    mactsta = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()

    results3 = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station==mactsta[0]).filter(Measurement.date<=s_date).all()

    #convert list of tuples into a normal list
    tobs_results = list(np.ravel(results3))

    session.close()

    return jsonify(tobs_results)

@app.route("/api/v1.0/datesearch/<startdate>")
def start(startdate):
    #create session link from python to the database
    session = Session(engine)
    
    #query
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results4 = (session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= startdate).group_by(Measurement.date).all())

    var_data = []
    for result in results4:
        d_dict = {}
        d_dict["Date"] = results4[0]
        d_dict["Low Temp"] = results4[1]
        d_dict["Avg Temp"] = results4[2]
        d_dict["High Temp"] = results4[3]
        var_data.append(d_dict)
 
    session.close()
       
    return jsonify(var_data)

@app.route("/api/v1.0/rangesearch/<startdate>/<enddate>")
def start_end(startdate, enddate):
    #create session link from python to the database
    session = Session(engine)
    
    """Return a list of miminum, average and maximum temperatures during date range"""
    #query stations
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results5 = (session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= startdate).filter(func.strftime("%Y-%m-%d", Measurement.date) <= enddate).group_by(Measurement.date).all())
    
    se_data = []
    for result in results5:
        j_dict = {}
        j_dict["Date"] = results5[0]
        j_dict["Low Temp"] = results5[1]
        j_dict["Avg Temp"] = results5[2]
        j_dict["High Temp"] = results5[3]
        se_data.append(j_dict)
        
    return jsonify(se_data)

    session.close()

#this needs to be present at the close of the file so this can be run in python using flask
if __name__=='__main__':
    app.run(debug=True)