# Import the dependencies.
from flask import Flask, jsonify, url_for

app = Flask(__name__)


#################################################
# Database Setup
#################################################


@app.route('/')
def homepage():
    """Homepage to list all available routes"""
    routes = {
        "homepage": url_for('homepage', _external=True),
        "most_active_stations": url_for('most_active_stations', _external=True),
        "temperature_statistics": url_for('temperature_statistics', _external=True),
        "temperature_histogram": url_for('temperature_histogram', _external=True)
    }
    return jsonify(routes)

@app.route('/most_active_stations')
def most_active_stations():
    """Endpoint to get the most active stations"""
    # Query for most active stations and return the result
    return "Most Active Stations"

@app.route('/temperature_statistics')
def temperature_statistics():
    """Endpoint to get temperature statistics"""
    # Query for temperature statistics and return the result
    return "Temperature Statistics"

@app.route('/temperature_histogram')
def temperature_histogram():
    """Endpoint to get temperature histogram"""
    # Query for temperature histogram and return the result
    return "Temperature Histogram"

@app.route('/api/v1.0/precipitation')
def precipitation():
    """Endpoint to retrieve the last 12 months of precipitation data"""
    # Calculate the date 12 months ago from the most recent date
    one_year_ago = most_recent_date - timedelta(days=365)
    
    # Query precipitation data for the last 12 months
    precipitation_data = session.query(measurement.date, measurement.prcp)\
        .filter(and_(measurement.date >= one_year_ago, measurement.date <= most_recent_date))\
        .all()
    
    # Convert the query results into a dictionary with date as key and precipitation as value
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_dict)


@app.route('/api/v1.0/stations')
def stations():
    """Endpoint to retrieve a JSON list of stations from the dataset"""
    # Query for all stations
    stations = session.query(measurement.station).distinct().all()
    
    # Convert the query results into a list
    station_list = [station[0] for station in stations]

    # Return the JSON representation of the list of stations
    return jsonify(station_list)


@app.route('/api/v1.0/tobs')
def tobs():
    """Endpoint to retrieve temperature observations of the most-active station for the previous year of data"""
    # Find the most active station
    most_active_station = most_active_stations_list[0][0]

    # Query temperature observations for the previous year for the most active station
    temperature_data = session.query(measurement.date, measurement.tobs)\
        .filter(measurement.station == most_active_station)\
        .filter(measurement.date >= one_year_ago)\
        .all()

    # Convert the query results into a list of dictionaries
    temperature_list = [{'date': date, 'temperature': tobs} for date, tobs in temperature_data]

    # Return the JSON representation of the list of temperature observations
    return jsonify(temperature_list)


@app.route('/api/v1.0/<start>')
def temperature_stats_start(start):
    """Endpoint to retrieve temperature statistics from a specified start date"""
    # Query temperature statistics from the start date
    temperature_stats = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
        .filter(measurement.date >= start)\
        .all()

    # Convert the query results into a dictionary
    temperature_stats_dict = {
        'start_date': start,
        'TMIN': temperature_stats[0][0],
        'TAVG': temperature_stats[0][1],
        'TMAX': temperature_stats[0][2]
    }

    # Return the JSON representation of the temperature statistics
    return jsonify(temperature_stats_dict)

# Define route for /api/v1.0/<start>/<end>
@app.route('/api/v1.0/<start>/<end>')
def temperature_stats_start_end(start, end):
    """Endpoint to retrieve temperature statistics from a specified start date to end date"""
    # Query temperature statistics from start date to end date
    temperature_stats = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
        .filter(measurement.date >= start)\
        .filter(measurement.date <= end)\
        .all()

    # Convert the query results into a dictionary
    temperature_stats_dict = {
        'start_date': start,
        'end_date': end,
        'TMIN': temperature_stats[0][0],
        'TAVG': temperature_stats[0][1],
        'TMAX': temperature_stats[0][2]
    }

    # Return the JSON representation of the temperature statistics
    return jsonify(temperature_stats_dict)

# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
if __name__ == '__main__':
    app.run(debug=True)