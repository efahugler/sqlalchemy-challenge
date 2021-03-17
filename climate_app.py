#Import Dependencies

import numpy as np 
import sqlalchemy
import datetime as dt 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker

# Python SQL toolkit and Object Relational Mapper
#Engine
engine = create_engine("sqlite:///hawaii.sqlite")
#Database into new model
Base = automap_base()
#Reflect Tables
Base.prepare(engine, reflect = True)

#Save table 
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session
session = Session(engine)

#Setup Flask
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start <br/>"
        f"/api/v1.0/<start>/<end> <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation(): 
    session = Session(engine)
    prcp_query = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= year_ago).\
    order_by(Measurement.date).all()
    precipitation = {}
    for result in prcp_query:
        prcp_list = {result.date: result.prcp, "prcp": result.prcp}
        precipitation.update(prcp_list)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations_total = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    station_list = list(np.ravel(stations_total))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs_total = session.query(Measurement.tobs).\
    filter(Measurement.date >= year_ago).\
    filter(Measurement.station == "USC00519281").\
    order_by(Measurement.date).all()
    tobs_query = list(np.ravel(tobs_total))
    return jsonify(tobs_query)

@app.route("/api/v1.0/temp/<start>")
def stats_temp(start): 
    #temperatures = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
    #filter(Measurement.station == most_active_station).all()
    #For the most active station
    #temp_query_demo = list(np.ravel(temperatures))
    #return jsonify(temp_query_demo)

    temp_query = session.query(Measurement.tobs).filter(Measurement.date >= recent_date).all()
    TMIN = temp_query.min()
    TAVG = temp_query.avg()
    TMAX = temp_query.max()
    stats = [TMIN, TAVG, TMAX]
    stats = list(np.ravel(stats))
    return jsonify(stats)

@app.route("/api/v1.0/temp/<start>/<end>")
def ending_time(start, end):
    end_query = session.query(Measurement.tobs).filter(Measurement.date >= recent_date).filter(Measurement.date <= first_date).all()
    TMIN = end_query.min()
    TAVG = end_query.avg()
    TMAX = end_query.max()
    stats_1 = [TMIN, TAVG, TMAX]
    stats_1 = list(np.ravel(stats_1))
    return jsonify(stats_1)
     

if __name__ == '__main__':
    app.run(debug=True)
