#Import Dependencies
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Create SQL engine
engine = create_engine("sqlite:///hawaii.sqlite")

#Reflect database
Base = automap_base()
Base.prepare(engine, reflect=True)

#Set table reference
Measurement = Base.classes.measurement
Station = Base.classes.station

########################
#Flask Setup
########################
app = Flask(__name__)

########################
#Flask Routes
########################
@app.route('/')
def home():
    return (
        f'<h1>Available Routes:</h1></br>'
        f'<ul>'
        f'<li>/api/v1.0/precipitation</li>'
        f'<li>/api/v1.0/stations</li>'
        f'<li>/api/v1.0/tobs</li>'
        f'<li>/api/v1.0/&#60start&#62</li>'
        f'<ul>'
        f'<li>Use yyyy-mm-dd notation</li>'
        f'</ul>'
        f'<li>/api/v1.0/&#60start&#62/&#60end&#62</li>'
        f'<ul>'
        f'<li>Use yyyy-mm-dd notation</li>'
        f'</ul>'
        f'</ul>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    session.close()

    precipitations = {}
    for result in results:
        date = str(result.date)
        precipitations[date] = result.prcp

    return jsonify(precipitations)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    results = session.query(Station).all()
    session.close()

    stations = []
    for result in results:
        station_dict = {}
        station_dict['id'] = result.id
        station_dict['station'] = result.station
        station_dict['name'] = result.name
        station_dict['latitude'] = result.latitude
        station_dict['longitude'] = result.longitude
        station_dict['elevation'] = result.elevation
        stations.append(station_dict)

    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
    session.close()

    tobs = {}
    for result in results:
        date = result.date
        tobs[date] = result.tobs
    
    return jsonify(tobs)

@app.route('/api/v1.0/<start>')
def start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    stats = {}
    for result in results:
        (min, max, avg) = result
        stats['min'] = min
        stats['max'] = max
        stats['avg'] = avg
    
    return jsonify(stats)

@app.route('/api/v1.0/<start>/<end>')
def startEnd(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date.between(start, end)).all()
    session.close()

    stats = {}
    for result in results:
        (min, max, avg) = result
        stats['min'] = min
        stats['max'] = max
        stats['avg'] = avg
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)