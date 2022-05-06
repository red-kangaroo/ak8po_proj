# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
from pandas import DataFrame
import requests
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, TIMESTAMP, VARCHAR, REAL
from time import sleep

from helper import set_logging, degrees_to_direction, insert_on_duplicate, ROOT

"""
AK8PO: Weather forecast

@author: Filip Findura
"""

# Software version:
VERSION = '0.2.2'
# Logging level:
LOG_LVL = 'INFO'
# Frequency of checking forecast (seconds):
LOOP_FREQ = 60*60  # hourly

# API requests:
REQ_URL = {
    "weatherapi": "http://api.weatherapi.com/v1/forecast.json?key={apikey}&q={loc}&days=7",
    "weatherstack": "http://api.weatherstack.com/forecast?access_key={apikey}&query={loc}&hourly=1&units=m",
    "nmi": "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}",
    "owm": "http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&"
           "exclude=minutely,daily&apikey={apikey}",
}
HEADER = {
    "user-agent": f"ak8po_weather.utb.cz/{VERSION}"
}
CONFIG = {
    "name": "Zlín",
    "lat": "49.22645",
    "lon": "17.67065",
}
KEYS = {  # TODO
    "weatherapi": "a47efd9e3c124cfaab591725222904",
    "weatherstack": "25ce89cb473ddcb5fe3451dfa181abdf",
    "owm": "c1470bca69b7132296d1dd941137a152",
}

# Database table columns:
COLUMNS = ['datasource', 'temperature', 'humidity', 'cloud_fraction', 'wind_speed', 'wind_dir', 'precipitations',
           'pressure', 'chance_rain', 'chance_snow']

# Database connection string (DBtype[+driver]://user:pwd@server/cat):
DB_USER = os.environ.get("AK8PO_USER", "ak8po")
DB_PWD = os.environ.get("AK8PO_PWD", "ak8po")
DB_HOST = os.environ.get("AK8PO_HOST", "localhost")
DB_NAME = os.environ.get("AK8PO_NAME", "weather")
DB_CON_STR = f"postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_NAME}"
DB_TABLE = "weather_data"
# Wait period for postgres in container to start
WAIT_FOR_DATABASE = 10
# Metadata for database structure:
Base = declarative_base()
# Database connection:
SQL = None
DB_ENG = None

# Unit conversion:
MPS_TO_KPH = 3.6


# ==============================================================================
# Database
# ==============================================================================
# class WeatherTable(Base):
#     # Tabulka se souhrnnymi daty za jednotlive roky
#     __tablename__ = DB_TABLE
#
#     forecast_time = Column(TIMESTAMP, nullable=False)
#     datasource = Column(VARCHAR(20), nullable=False)
#     temperature = Column(REAL)
#     humidity = Column(REAL)
#     cloud_fraction = Column(REAL)
#     wind_speed = Column(REAL)
#     wind_dir = Column(VARCHAR(4))
#     precipitations = Column(REAL)
#     pressure = Column(REAL)
#     chance_rain = Column(REAL)
#     chance_snow = Column(REAL)


def open_session():
    global SQL, DB_ENG

    try:
        engine = sqlalchemy.create_engine(DB_CON_STR)
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        session = Session()

        DB_ENG = engine
        SQL = session
    except Exception as e:
        if ROOT is not None:
            ROOT.error(f"Failed to establish SQL connection: {e}")
        else:
            print(e)


def close_session():
    global SQL, DB_ENG

    if SQL is None and DB_ENG is None:
        return
    else:
        try:
            engine = SQL.get_bind()
            SQL.close()
            engine.dispose()
        except Exception as e:
            if ROOT is not None:
                ROOT.error(f"Failed to relinquish SQL connection: {e}")
            else:
                print(e)

    DB_ENG = None
    SQL = None


# ==============================================================================
# Forecast
# ==============================================================================
class WeatherReader:
    def __init__(self, w_name, w_logger):
        self.name = w_name
        self.logger = w_logger

        self.logger.info(f"Weather forecast reader version {VERSION} is starting...")
        self.loop = True

    def main_loop(self):
        """Main module loop

        Ends on Ctrl+C.
        """
        # Let Postgres start before we do anything rash:
        sleep(WAIT_FOR_DATABASE)

        try:
            while self.loop:
                ok = True

                try:
                    time_start = datetime.datetime.now()

                    self.logger.info("Reading data...")
                    in_data = self.get_data()

                    self.logger.info("Writing data...")
                    for s in in_data.keys():
                        try:
                            ok &= self.set_data(s, in_data[s])
                        except Exception as e:
                            self.logger.error(f"Unhandled exception when writing data: {e}")

                    time_elapsed = datetime.datetime.now() - time_start
                    self.logger.info(f"Finished forecast scraping in {time_elapsed.total_seconds():.3f} seconds.")
                except Exception as e:
                    self.logger.error(f"Failed a forecast gathering cycle: {e}")

                # if not ok:
                #     self.logger.warning("Forecast gathering had some problems.")

                # Sleep until the next cycle:
                sleep(LOOP_FREQ)

        except KeyboardInterrupt:
            self.loop = False

        self.logger.info("Module terminated.")

    def get_data(self) -> dict:
        """Read all data

        Calls APIs for all sources and returns the data.

        :returns: dict(source str: data dict)
        """
        in_data = dict()

        for source in REQ_URL.keys():
            try:
                in_data[source] = self.call_api(source)
            except Exception as e:
                self.logger.error(f"Failed to read from source {source}: {e}")

        return in_data

    def set_data(self, source: str, in_data: dict) -> bool:
        """Write all data

        Processes data for each source, then writes them to database.
        """
        global SQL, DB_ENG, DB_TABLE

        # Call specific processing method for each source:
        try:
            table: DataFrame = getattr(self, f"process_{source.lower()}")(in_data)
        except Exception as e:
            self.logger.error(f"Could not process data for source {source}: {e}")
            return False

        # Write to database:
        open_session()
        if SQL is None:
            self.logger.error("No SQL connection available.")
            return False

        try:
            ok = table.to_sql(DB_TABLE, DB_ENG, if_exists='append', index_label='forecast_time',
                              method=insert_on_duplicate)  # INSERT
            # Returns True if the INSERT affected the same number of rows as are found in the DataFrame. Otherwise some
            # data were likely missed/dropped, so return False.
            ok = ok == len(table.index)
        except Exception as e:
            ok = False
            self.logger.error(f"Could not write data to SQL: {e}")

        close_session()
        if SQL is not None:
            self.logger.warning("SQL connection not closed properly.")

        return ok

    def process_weatherapi(self, in_data: dict) -> DataFrame:
        """Process data for Weather API

        :returns: DataFrame indexed by timestamp
        """
        source = "weatherapi"
        day_data = in_data['forecast']['forecastday']
        out_data = list()
        index = list()

        for d in day_data:
            for h in d['hour']:
                try:
                    index.append(h['time'])

                    new_row = list()
                    new_row.append(source)
                    # new_row.append(h['time'])
                    new_row.append(h['temp_c'])
                    new_row.append(h['humidity'])
                    new_row.append(h['cloud'])
                    new_row.append(h['wind_kph'])
                    new_row.append(h['wind_dir'])
                    new_row.append(h['precip_mm'])
                    new_row.append(h['pressure_mb'])
                    new_row.append(h['chance_of_rain'])
                    new_row.append(h['chance_of_snow'])

                    out_data.append(new_row)
                except Exception as e:
                    self.logger.warning(f"Could not add a new row for {source}: {e}")

        table = DataFrame(data=out_data, index=index, columns=COLUMNS)
        return table

    @staticmethod
    def process_weatherstack(in_data: dict) -> DataFrame:
        """Process data for WeatherStack

        :returns: DataFrame indexed by timestamp
        """
        source = "weatherstack"
        day_data = in_data['current']
        out_data = list()
        index = list()
        index.append(in_data['location']['localtime'])  # TODO: Round to nearest hour.

        new_row = list()
        new_row.append(source)
        # new_row.append(h['time'])
        new_row.append(day_data['temperature'])
        new_row.append(day_data['humidity'])
        new_row.append(day_data['cloudcover'])
        new_row.append(day_data['wind_speed'])
        new_row.append(day_data['wind_dir'])
        new_row.append(day_data['precip'])
        new_row.append(day_data['pressure'])
        new_row.append(None)  # chance_of_rain
        new_row.append(None)  # chance_of_snow

        out_data.append(new_row)

        table = DataFrame(data=out_data, index=index, columns=COLUMNS)
        return table

    def process_nmi(self, in_data: dict) -> DataFrame:
        """Process data for Norwegian Meteorological Institute

        :returns: DataFrame indexed by timestamp
        """
        source = "nmi"
        ts = in_data['properties']['timeseries']
        out_data = list()
        index = list()

        for dataset in ts:
            index.append(dataset['time'])

            try:
                samples = dataset['data']['instant']['details']
            except Exception as e:
                self.logger.warning(f"Could not read samples: {e}")
                continue

            # Get all needed values:
            air_temp = samples['air_temperature']
            air_pressure = samples['air_pressure_at_sea_level']
            cloud_area = samples['cloud_area_fraction']
            wind_dir = degrees_to_direction(int(samples['wind_from_direction']))
            wind_speed = samples['wind_speed'] * MPS_TO_KPH
            humidity = samples['relative_humidity']

            # Precipitation is always for the next hour, i.e. the value means "from now till the next our"
            try:
                precipitation = dataset['data']['next_1_hours']['details']['precipitation_amount']
            except KeyError:
                precipitation = 0.0
            except Exception as e:
                self.logger.warning(f"Precipitation not found: {e}")
                precipitation = None

            # Add the data into the dataset
            out_data.append([source, air_temp, humidity, cloud_area, wind_speed, wind_dir, precipitation,
                             air_pressure, None, None])  # Last two are chance of rain and snow.

        table = DataFrame(data=out_data, index=index, columns=COLUMNS)
        return table

    def process_owm(self, in_data: dict) -> DataFrame:
        """Process data for OpenWeatherMap

        :returns: DataFrame indexed by timestamp
        """
        source = "owm"
        hour_data = in_data['hourly']
        out_data = list()
        index = list()

        for h in hour_data:
            try:
                index.append(datetime.datetime.fromtimestamp(h['dt']))

                new_row = list()
                new_row.append(source)
                new_row.append(h['temp'])
                new_row.append(h['humidity'])
                new_row.append(h['clouds'])
                new_row.append(h['wind_speed'] * MPS_TO_KPH)
                new_row.append(degrees_to_direction(int(h['wind_deg'])))
                try:
                    new_row.append(h['rain']['1h'])
                except KeyError:
                    new_row.append(None)
                new_row.append(h['pressure'])
                new_row.append(None)  # chance_of_rain
                new_row.append(None)  # chance_of_snow

                out_data.append(new_row)
            except Exception as e:
                self.logger.warning(f"Could not add a new row for {source}: {e}")

        table = DataFrame(data=out_data, index=index, columns=COLUMNS)
        return table

    def call_api(self, source: str) -> dict:
        """Request data from source

        :returns: Dictionary of the JSON with data.
        """
        out_data = dict()

        url = REQ_URL.get(source, None)
        if url is None:
            self.logger.error(f"Unsupported source {source}, cannot read forecast.")
            return out_data
        else:
            url = url.replace('{lat}', CONFIG["lat"])
            url = url.replace('{lon}', CONFIG["lon"])
            url = url.replace('{loc}', CONFIG["name"])
            # Also set API key, which won't matter when there is no apikey to replace:
            url = url.replace('{apikey}', KEYS.get(source, ""))

        self.logger.debug(f'Calling the API: {url}')
        response = requests.get(url, headers=HEADER)
        if response.status_code != 200:
            self.logger.warning(f"Request failed when contacting {source} forecast API: {response.reason}")
            return out_data
        out_data = response.json()

        return out_data


# ==============================================================================
# Entrypoint
# ==============================================================================
if __name__ == "__main__":
    name = "weather"
    logger = set_logging(name, LOG_LVL)

    try:
        wr = WeatherReader(name, logger)
        wr.main_loop()
    except Exception as ex:
        logger.critical(f"Service terminated on error: {ex}")
