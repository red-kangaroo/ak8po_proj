# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from pandas import DataFrame
import requests
from time import sleep

from helper import set_logging, degrees_to_direction

"""
AK8PO: Weather forecast

@author: Filip Findura
"""

# Software version:
VERSION = '0.1.0'
# Logging level:
LOG_LVL = 'DEBUG'
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
KEYS = {
    "weatherapi": "a47efd9e3c124cfaab591725222904",
    "weatherstack": "25ce89cb473ddcb5fe3451dfa181abdf",
    "owm": "c1470bca69b7132296d1dd941137a152",
}

# Database table columns:
COLUMNS = ['source', 'temperature', 'humidity', 'cloud_fraction', 'wind_speed', 'wind_dir', 'precipitations',
           'pressure', 'chance_rain', 'chance_snow']


# ==============================================================================
# Functionality
# ==============================================================================
class WeatherReader:
    def __init__(self, w_name, w_logger):
        self.name = w_name
        self.logger = w_logger
        self.logger.info(f"Weather forecast reader version {VERSION} is starting...")

        # Create database connection:
        # self.db = Database(
        #     host=self.config.db_host,
        #     user=self.config.get('db_user'),
        #     pwd=self.config.get('db_password'),
        #     cat=self.config.db_cat,
        #     log=self.logger
        # )

        self.loop = True

    def main_loop(self):
        """Main module loop

        Ends on Ctrl+C.
        """
        try:
            while self.loop:
                # TODO
                in_data = self.get_data()

                for s in in_data.keys():
                    self.set_data(s, in_data[s])

                sleep(LOOP_FREQ)
        except KeyboardInterrupt:
            self.loop = False

        self.logger.info("Module terminated.")

    def get_data(self) -> dict:
        """Read all data

        Calls APIs for all sources and returns the data.

        :returns: dict(source str: data dict)
        """
        self.logger.info("Reading data...")
        in_data = dict()

        for source in REQ_URL.keys():
            in_data[source] = self.call_api(source)

        return in_data

    def set_data(self, source: str, in_data: dict) -> bool:
        """Write all data

        Processes data for each source, then writes them to database.
        """
        ok = True
        self.logger.info("Writing data...")

        # Call specific processing method for each source:
        try:
            table = getattr(self, f"process_{source.lower()}")(in_data[source.lower()])
        except Exception as e:
            self.logger.error(f"Could not process data for source {source}: {e}")
            return False

        # Write to database:
        self.db.set(self.config.db_measurement, table)

        return ok

    @staticmethod
    def process_weatherapi(in_data: dict) -> DataFrame:
        """Process data for Weather API

        :returns: DataFrame indexed by timestamp
        """
        source = "weatherapi"
        day_data = in_data['forecast']['forecastday']
        out_data = list()
        index = list()

        for d in day_data:
            for h in d['hour']:
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
        index.append(in_data['location']['localtime'])

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
            wind_speed = samples['wind_speed']
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

    @staticmethod
    def process_owm(in_data: dict) -> DataFrame:
        """Process data for OpenWeatherMap

        :returns: DataFrame indexed by timestamp
        """
        source = "owm"
        hour_data = in_data['hourly']
        out_data = list()
        index = list()

        for h in hour_data:
            index.append(datetime.datetime.fromtimestamp(h['dt']))

            new_row = list()
            new_row.append(source)
            new_row.append(h['temp'])
            new_row.append(h['humidity'])
            new_row.append(h['clouds'])
            new_row.append(h['wind_speed'])
            new_row.append(degrees_to_direction(int(h['wind_deg'])))
            try:
                new_row.append(h['rain']['1h'])
            except KeyError:
                new_row.append(None)
            new_row.append(h['pressure'])
            new_row.append(None)  # chance_of_rain
            new_row.append(None)  # chance_of_snow

            out_data.append(new_row)

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
        # TODO
        data = wr.get_data()
        wr.set_data('nmi', data)
        print(data)
        # wr.main_loop()
    except Exception as ex:
        logger.critical(f'Service terminated on error: {ex}')
