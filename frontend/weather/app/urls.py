from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_search, name='weathersearch'),
    # path('saleslist', views.SalesListView.as_view(), name='weatherlist')
]
