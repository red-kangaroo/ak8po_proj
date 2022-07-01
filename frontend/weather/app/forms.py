from django import forms

CHART_CHOICES = (
    ('bar', 'Bar Chart'),
    ('pie', 'Pie Chart'),
    ('line', 'Line Chart')
)
RESULTS_CHOICES = (
    ('datasource', 'Data Source'),
    ('forecast_time', 'Forecast Time')
)


class WeatherSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
    order_by = forms.ChoiceField(choices=RESULTS_CHOICES)
