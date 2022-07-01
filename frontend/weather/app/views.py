# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib import messages
import pandas

from .forms import WeatherSearchForm
from .models import *
from .utils import get_chart

"""
AK8PO: Request handling

@author: Filip Findura
"""


def weather_search(request):
    weather_df = None
    chart = None
    no_data = None
    search_form = WeatherSearchForm(request.POST or None)

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        order_by = request.POST.get('order_by')

        # print(date_from, date_to, chart_type)
        weather_query = WeatherData.objects.filter(forecast_time__date__lte=date_to,
                                                   forecast_time__date__gte=date_from)

        if len(weather_query) > 0:
            weather_df = pandas.DataFrame(weather_query.values())
            # print(weather_df)

            # sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%d/%m/%Y'))
            weather_df.rename({'wind_dir': 'wind direction', },
                              axis=1, inplace=True)

            chart, msg = get_chart(chart_type, weather_df, order_by)
            weather_df = weather_df.to_html()

            if len(msg) > 0:
                for m in msg:
                    messages.warning(request, m)
        else:
            messages.warning(request, "No data available.")

    context = {
        'search_form': search_form,
        'weather_df': weather_df,
        'chart': chart,
    }
    return render(request, 'weather_search.html',  context)
