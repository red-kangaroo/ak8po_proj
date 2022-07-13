from django import forms
from crispy_forms.layout import Div, Field
from crispy_forms.helper import FormHelper, Layout


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


class WeatherSearchForm(forms.Form):
    helper = FormHelper()
    helper.layout = Layout(
        Div(Field('date_from'), Field('date_to'),
            css_class='form-row'),
        Div(Field('chart_source'), Field('chart_data'),
            css_class='form-row'),
    )

    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    chart_source = forms.MultipleChoiceField(choices=SOURCE_CHOICES, widget=forms.CheckboxSelectMultiple,
                                             initial=[c[0] for c in SOURCE_CHOICES])
    chart_data = forms.MultipleChoiceField(choices=DATA_CHOICES, widget=forms.CheckboxSelectMultiple,
                                           initial=[c[0] for c in DATA_CHOICES])
