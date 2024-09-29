# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import datetime as dt
from datetime import datetime, timedelta

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Users/genna/Desktop/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>(Custom date)<br/>"
        f"/api/v1.0/<start>(Start date)/<end>(End date)<br/>"
        f"<br/>"
        f"<br/>"
        f"Please make sure to enter any desired date in YYYY-MM-DD format! :)"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    """Return a dictionary of the last 12 months worth of precipitation data."""
    # Query all data
    recent = session.query(func.max(measurement.date)).scalar()
    recent_date = datetime.strptime(recent, '%Y-%m-%d')
    last_year = recent_date - timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_year).all()

    # Create a dictionary with date as the key and prcp as the value
    prcp_dict = {date: prcp for date, prcp in results}

    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():

    """Return a JSON list of stations from the dataset."""
    # Query all data
    results = session.query(station.station).all()

    # Convert list of tuples into normal list
    id = list(np.ravel(results))

    return jsonify(id)


@app.route("/api/v1.0/tobs")
def tobs():

    """Return a JSON list of temperature observations for the previous year."""
    # Query all data
    recent = session.query(func.max(measurement.date)).scalar()
    recent_date = datetime.strptime(recent, '%Y-%m-%d')
    last_year = recent_date - timedelta(days=365)

    # results = session.query(station.station).all()
    results = session.query(measurement.tobs).filter(
    measurement.date >= last_year,
    measurement.station == 'USC00519281'
).order_by(measurement.tobs).all()
    # Convert list of tuples into normal list
    
    tobs = list(np.ravel(results))

    return jsonify(tobs)


@app.route("/api/v1.0/<start>", methods=['GET'])
def get_temperatures(start):

    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start range."""
    # Query all data
    start_date = datetime.strptime(start, '%Y-%m-%d')

    # Query for min, avg, and max temperatures from the start date to the most recent date
    results = session.query(
        func.min(measurement.tobs),
        func.avg(measurement.tobs),
        func.max(measurement.tobs)
    ).filter(measurement.date >= start_date).all()

    min_temp, avg_temp, max_temp = results[0]

    # Create a response dictionary
    response = {
        'start_date': start,
        'min_temp': min_temp,
        'avg_temp': avg_temp,
        'max_temp': max_temp
    }

    return jsonify(response)


@app.route("/api/v1.0/<start>/<end>", methods=['GET'])
def get_more_temperatures(start, end):

    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start range."""
    # Query all data
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')

    # Query for min, avg, and max temperatures from the start date to the most recent date
    results = session.query(
        func.min(measurement.tobs),
        func.avg(measurement.tobs),
        func.max(measurement.tobs)
    ).filter(measurement.date >= start_date, measurement.date <= end_date).all()

    min_temp, avg_temp, max_temp = results[0]

    # Create a response dictionary
    response = {
        'start_date': start,
        'min_temp': min_temp,
        'avg_temp': avg_temp,
        'max_temp': max_temp
    }

    return jsonify(response)


session.close()

if __name__ == '__main__':
    app.run(debug=True)
