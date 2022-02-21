# %%
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

# %%
import numpy as np
import pandas as pd
import datetime as dt

# %% [markdown]
# # Reflect Tables into SQLAlchemy ORM

# %%
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.declarative import declarative_base

# %%
#? what is diference from sqlite vs csv file | we can't read anything in sqlite, sqlite is a database file
#? create engine and connect is to connect the sqlite database to any apps using Python languages)
## step 1: data_path -> read that path by pd.read_sql() or engine.execute("select * from hwaii",connect) 
## step 2: create engine -> engine = create_engine(f"sqlite:///{data_path}") | engine = create_engine("sqlite://hawaii.sqlite")
## step 3: connect engine by connect = engine.connect() | if we wanna use Pandas for next steps, the object can be paste to Pandas
# Base = before going to define the Class |table 
# when to use DB Browser? to read sqlite file, to browse the sqlite file or even create table. 
# use session.query() is to call data from the file


# %%
# create engine to hawaii.sqlite | create a virtual database itself to do further step here 

database_path = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")
# engine = create_engine("sqlite:///hawaii.sqlite")
# Base = declarative_base()

# %%
# reflect an existing database into a new model: sqlite is a database containing 2 tables that we connect then reflect them now
# ref. day 2, student reflection activity 
connect = engine.connect()
data_measurement = engine.execute("SELECT * FROM measurement")
data_station = engine.execute("SELECT * FROM station")

# %%
# View all of the classes that automap found : reflect 2 table available in DB Browser (measurement | station)
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

# %%
# Save references to each table : class | bcoz the 2 tables are already available -> 
# no need to create Class __table__ : simpler way here is to use Base.classes.table_name
measurement = Base.classes.measurement
station = Base.classes.station

# %%
# Create our session (link) from Python to the DB : refer day 2 , 1 or 2 activity 
# purpose of this session? 
session = Session(engine)


# %% [markdown]
# # Exploratory Precipitation Analysis

# %%
# Find the most recent date in the data set.
session.query(measurement.date).order_by(measurement.date.desc()).first()

# %%
# Earliest Date
session.query(measurement.date).order_by(measurement.date).first()

# %%
# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
# Starting from the most recent data point in the database. 
# How to retrieve data in 2017 only? or between the 2 given dates 


# %%
import datetime as dt

# %%
# Calculate the date one year from the last date in data set.
oneyear_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
print("Date since one year from the last day is: ", oneyear_date)

# %%
# Get a list of column names and types for reference first
inspector = inspect(engine)
inspector.get_table_names()
columns = inspector.get_columns('measurement')
for c in columns:
    print(c['name'], c["type"])

# %%
# same task with station table
inspector = inspect(engine)
inspector.get_table_names()
columns1 = inspector.get_columns('station')
for c in columns1:
    print(c['name'], c["type"])

# %%
# Perform a query to retrieve the data and precipitation scores from measuremnt table
# opt 1: call all data without limit timing

tracie1 = session.query(measurement.date, measurement.prcp).all()

#write into a df to have pretty view
panda1 = pd.DataFrame(tracie1,columns = ["Date","Rainfall"])
panda1

# %%
# Perform a query to retrieve the data and precipitation scores
# for the most recent 12 months
precip = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= oneyear_date).all()
precip

# %%
precip_df = pd.DataFrame(precip, columns = ["Date","Rainfall"])
precip_df

# %%
precip_sort = precip_df.sort_values("Date")
precip_sort

# %%
# plotting using pandas
precip_sort.plot(x="Date",y="Rainfall",rot = 90)
plt.xlabel("Date")
plt.ylabel("Precipitation")
plt.title("The Preciptation of the most recent year")
plt.show()

# %%
# Use Pandas to calculate the summary statistics for the precipitation data 
precip_df.describe()

# %%
# try one kind of query with condition
session.query(measurement.station,measurement.prcp,measurement.date).\
    filter(measurement.date < '2017-08-23').\
    order_by(measurement.date).limit(10).all()

# %% [markdown]
# # Exploratory Station Analysis

# %%
# JOIN 2 tables to get master data file

master = [measurement.id, station.id, measurement.station, station.station]
same_station = session.query(*master).filter(measurement.station == station.station).all()
master

# %%
common_station = pd.DataFrame(same_station, columns = ["id1","id2","stat1","stat2"])
common_station

# %%
common = len(same_station)
print(common)

# %%
# Design a query to calculate the total number stations in the dataset
# JOIN 2 tables to get all station or get each table station then + each other

sta1 = session.query(station.station).count()
sta2 = session.query(measurement.station).count()
print(sta2+sta1-common)

# %%
# another shorten query to get non-duplicated rows in station; 

# %%
# drop duplicated row by SELECT DISTINCT 
station1 = session.execute('SELECT DISTINCT station from station').fetchall()
len(station1)

# %%
# SAME CODE FOR MEASUREMENT TABLE
station2 = session.execute('SELECT DISTINCT station from measurement').fetchall()
len(station2)

# %%
# reference the station1 and station 2 having same station names
print(f" there are total {len(station1)} stations in the data set")

# %%
# Design a query to find the most active stations (i.e. what stations have the most rows?)

group = session.query(measurement.station, measurement.id, func.count(measurement.station)).\
    group_by(measurement.station).all()

active_station_list = pd.DataFrame(group,columns = ["station","ID","value_count"])
active_station_list


# %%
# the most active station |
active_station = active_station_list["value_count"].max()
active_station	

# %%
print(f"the station with total {active_station} rows is the most active one. USC00519281 | id: 12188")

# %%
# List the stations and the counts in descending order.

station_sort = active_station_list.sort_values("value_count",ascending=False)
station_sort

# %%
from scipy import stats
from numpy import mean
import pandas as pd

# %%
# groupby station df and retrieve the temperature observations in: max | min | avg
# find the highest temperature per station
tobs_max = session.query(measurement.station, measurement.tobs,func.max(measurement.tobs)).\
    group_by(measurement.station).all()
tobs_max

# %%
# find the lowest temperature per station
tobs_min = session.query(measurement.station, measurement.tobs,func.min(measurement.tobs)).\
    group_by(measurement.station).all()
tobs_min

# %%
# find the average temperature per station
tobs_avg = session.query(measurement.station, measurement.tobs,func.avg(measurement.tobs)).\
    group_by(measurement.station).all()
tobs_avg

# %%
# Query the last 12 months of temperature observation (tobs) data for this station
# groupby station with 2 conditions (filter) to get those data
# oneyear_date = 2016-08-23

tobs_df1 = session.query(measurement.station, measurement.tobs, measurement.date).\
    filter(measurement.station == 'USC00519281').filter(measurement.date >= oneyear_date).all()
tobs_df1

# %%
# do for loop to get a list of temperature observations (tobs) for plotting
# btw filter out null values from tobs lists
temp_list = []
for temp in tobs_df1:
    if type(temp.tobs) == float:
        temp_list.append(temp.tobs)
print(temp_list)

# %%
from jupyterthemes import jtplot
jtplot.style(theme = 'grade3', context= 'notebook', ticks=True, grid=False)

# %%
# plot the results as a histogram style

plt.hist(temp_list, bins= 12, range=None, density=False, weights=None, cumulative=False, bottom=None, histtype='bar', 
        align='mid', orientation='vertical', rwidth=None, log=False, color=None, label=None, stacked=False,
        )
plt.xlabel("Temperature observations")
plt.ylabel("Frequency")
plt.title("The Most Active Station Temperature Observation")
plt.grid(axis = "y")
plt.show()


# %%
# in the most active station observation:
#  - the highest temperature is: 
#   - the lowest temperature is: 
#   - the average temperature is: 
#   - the most frequent temperature is from 75F - 77F; next is from 72.5F to 74F

# %% [markdown]
# # Close session

# %%
# Close Session
session.close()

# %%



