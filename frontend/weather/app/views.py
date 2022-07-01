# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from django.shortcuts import render
from django.contrib import messages
import pandas
from pretty_html_table import build_table

from .forms import WeatherSearchForm
from .models import *
from .utils import get_chart

"""
AK8PO: Request handling

@author: Filip Findura
"""


def weather_search(request):
    chart = None
    html_table = None
    search_form = WeatherSearchForm(request.POST or None)
    # messages.set_level(request, messages.DEBUG)  # TODO

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        order_by = request.POST.get('order_by')

        weather_query = WeatherData.objects.filter(forecast_time__date__lte=date_to,
                                                   forecast_time__date__gte=date_from)

        if len(weather_query) > 0:
            weather_df = pandas.DataFrame(weather_query.values())
            chart, msg = get_chart(chart_type, weather_df, order_by)

            # weather_df['created'] = weather_df['created'].apply(lambda x: x.strftime('%d/%m/%Y'))
            weather_df.rename({
                'forecast_time': 'Date & Time',
                'datasource': 'Data Source',
                'temperature': 'Temperature (°C)',
                'humidity': 'Humidity (%)',
                'cloud_fraction': 'Cloudiness (%)',
                'wind_speed': 'Wind Speed (km/h)',
                'wind_dir': 'Wind Direction',
                'precipitations': 'Precipitation (mm)',
                'pressure': 'Pressure (mb)',
                'chance_rain': 'Chance of Rain (%)',
                'chance_snow': 'Chance of Snow (%)',
            },
                              axis=1, inplace=True)
            # Use a nicer table than the basic one that Pandas can construct:
            # weather_df = weather_df.to_html()
            html_table = build_table(weather_df, 'blue_light', text_align='center', even_color='f7f7f7',
                                     conditions={
                                         'Precipitation (mm)': {
                                             # 'min': 25,
                                             # 'min_color': 'green',
                                             'max': 0.0,
                                             'max_color': 'red',
                                         }
                                     })
            # See https://pypi.org/project/pretty-html-table/

            if len(msg) > 0:
                for m in msg:
                    messages.warning(request, m)
        else:
            date_min = datetime.datetime.strptime(date_from, "%Y-%m-%d")
            date_max = datetime.datetime.strptime(date_to, "%Y-%m-%d")

            if date_max < date_min:
                messages.error(request, "Date From must be lower or equal to Date To.")
            else:
                messages.warning(request, "No data available.")

    context = {
        'search_form': search_form,
        'weather_df': html_table,
        'chart': chart,
    }
    return render(request, 'weather_search.html',  context)
