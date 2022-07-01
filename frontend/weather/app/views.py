# import pandas
from django.shortcuts import render
from django.views.generic import ListView
from .forms import WeatherSearchForm


def weather_search(request):
    search_form = WeatherSearchForm(request.POST or None)
    context = {
        'search_form': search_form,
    }
    return render(request, 'weather_search.html',  context)
