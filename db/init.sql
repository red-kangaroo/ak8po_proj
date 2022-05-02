-- Create tables if there are none, otherwise delete data currently in it.
CREATE TABLE IF NOT EXISTS weather_data(
        forecast_time timestamp not null,
        datasource varchar(20) not null,
        temperature real null,
        humidity real null,
        cloud_fraction real null,
        wind_speed real null,
        wind_dir varchar(4) null,
        precipitations real null,
        pressure real null,
        chance_rain real null,
        chance_snow real null
      );
DELETE FROM weather_data;
