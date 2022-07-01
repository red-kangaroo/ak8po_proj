# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class WeatherData(models.Model):
    forecast_time = models.DateTimeField(primary_key=True)
    datasource = models.CharField(max_length=20)
    temperature = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    cloud_fraction = models.FloatField(blank=True, null=True)
    wind_speed = models.FloatField(blank=True, null=True)
    wind_dir = models.CharField(max_length=4, blank=True, null=True)
    precipitations = models.FloatField(blank=True, null=True)
    pressure = models.FloatField(blank=True, null=True)
    chance_rain = models.FloatField(blank=True, null=True)
    chance_snow = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weather_data'
        unique_together = (('forecast_time', 'datasource'),)
