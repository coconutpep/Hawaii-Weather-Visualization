#Import Dependencies
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Create SQL engine
engine = create_engine("sqlite:///hawaii.sqlite")

#Reflect database
Base = automap_base()
Base.prepare(engine, reflect=True)

#Set table reference
Measurement = Base.classes.measurement
Station = Base.classes.station