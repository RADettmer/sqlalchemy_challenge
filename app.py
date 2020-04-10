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
Mea = Base.classes.measurement
Sta = Base.classes.station

#create session link to the database to generate starting and ending dates
session = Session(engine)

#create end of search query - final date
f_date = session.query(func.max(func.strftime("%Y-%m-%d", Mea.date))).all()
max_date_str = f_date[0][0]
max_date = dt.datetime.strptime(max_date_str, "%Y-%m-%d")
#create beginning of search query - start date - calculated for a one year period
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
        f"/api/v1.0/datesearch/2016-10-13<br/>"
        f"/api/v1.0/rangesearch/2016-10-14/2017-11-14"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session link from python to the database
    session = Session(engine)
       
    """Return dates and precipitiation amounts for specific date range"""
    #query all precipitation amounts for specific date range
    results1 = session.query(func.strftime("%Y-%m-%d", Mea.date), Mea.prcp).\
        filter(func.strftime("%Y-%m-%d", Mea.date) >= s_date).all()

    """Convert the query results to a dictionary using date as the key and prcp as the value"""       
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
    results2 = session.query(Sta.station, Sta.name).all()

    #convert list of tuples into a normal list
    sta_names = list(np.ravel(results2))
    
    session.close()

    return jsonify(sta_names)

@app.route("/api/v1.0/tobs")
def tobs():
    #create session link from python to the database
    session = Session(engine)

    #query tobs for last year of data for most active station
    mactsta = session.query(Mea.station, func.count(Mea.station)).group_by(Mea.station).order_by(func.count(Mea.station).desc()).first()

    results3 = session.query(Mea.date, Mea.tobs).filter(Mea.station==mactsta[0]).filter(Mea.date<=s_date).all()

    #convert list of tuples into a normal list
    tobs_results = list(np.ravel(results3))

    session.close()

    return jsonify(tobs_results)

@app.route("/api/v1.0/datesearch/<startdate>")
def start(startdate):
    #create session link from python to the database
    session = Session(engine)

    """Return a list of miminum, average and maximum temperatures geater than start tdate"""
    #query measurements for data greater than or equal to start date - 2016-10-13
    sel = [Mea.date, func.min(Mea.tobs), func.avg(Mea.tobs), func.max(Mea.tobs)]
    results4 = (session.query(*sel).filter(func.strftime("%Y-%m-%d", Mea.date) >= startdate).group_by(Mea.date).all())

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
    
    """Return a list of miminum, average and maximum temperatures during between date range"""
    #query measurements for specific date range - 2016-10-07 thru 2016-11-14
    sel = [Mea.date, func.min(Mea.tobs), func.avg(Mea.tobs), func.max(Mea.tobs)]
    results5 = (session.query(*sel).filter(func.strftime("%Y-%m-%d", Mea.date) >= startdate).filter(func.strftime("%Y-%m-%d", Mea.date) <= enddate).group_by(Mea.date).all())
    
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