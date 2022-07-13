# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from django import forms
from crispy_forms.layout import Div, Field
from crispy_forms.helper import FormHelper, Layout

"""
AK8PO: Web forms

@author: Filip Findura
"""

SOURCE_CHOICES = (
    ('nmi', 'Norwegian Meteorological Institute'),
    ('owm', 'Open Weather Map'),
    ('weatherapi', 'Weather API'),
    ('weatherstack', 'Weather Stack'),
)
DATA_CHOICES = (
    ('temperature', 'Temperature'),
    ('humidity', 'Humidity'),
    ('cloud_fraction', 'Cloudiness'),
    ('wind_speed', 'Wind Speed'),
    # ('wind_dir', 'Wind Direction'),
    ('precipitations', 'Precipitation'),
    ('pressure', 'Pressure'),
    ('chance_rain', 'Chance of Rain'),
    ('chance_snow', 'Chance of Snow'),
)
DATA_DEFAULT = ['temperature', 'humidity', 'precipitations']
DATE_NOW = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")


# ==============================================================================
# Forms
# ==============================================================================
class WeatherSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=DATE_NOW)
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=DATE_NOW)
    chart_source = forms.MultipleChoiceField(choices=SOURCE_CHOICES, widget=forms.CheckboxSelectMultiple,
                                             initial=[c[0] for c in SOURCE_CHOICES], required=False)
    chart_data = forms.MultipleChoiceField(choices=DATA_CHOICES, widget=forms.CheckboxSelectMultiple,
                                           initial=DATA_DEFAULT, required=False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Div(Field('date_from'), Field('date_to'),
    #             css_class='form-row'),
    #         Div(Field('chart_source'), Field('chart_data'),
    #             css_class='form-row'),
    #     )
