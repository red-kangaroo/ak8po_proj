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
        chance_snow real null,
        PRIMARY KEY (forecast_time, datasource)
      );
DELETE FROM weather_data;

DROP ROLE IF EXISTS ak8po;
CREATE ROLE ak8po WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  ENCRYPTED PASSWORD 'md5caf27c6a8890c201031c91036dd7a80e';
GRANT pg_read_all_settings, pg_read_all_stats, pg_read_server_files, pg_write_server_files TO ak8po;

ALTER TABLE weather_data OWNER TO ak8po;
