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
        f'Available Routes:</br>'
        f'<ul>'
        f'<li>/api/v1.0/precipitation</li></br>'
        f'<li>/api/v1.0/stations</li><br>'
        f'<li>/api/v1.0/tobs</li></br>'
        f'<li>/api/v1.0/&#60start&#62</li></br>'
        f'<li>/api/v1.0/&#60start&#62/&#60end&#62</li></br>'
        f'</ul>'
    )

if __name__ == '__main__':
    app.run(debug=True)