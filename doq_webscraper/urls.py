from django.urls import path

from . import views

urlpatterns = [
    path('doq_webscraper', views.nifty_fifty, name="doq_webscraper"),
]