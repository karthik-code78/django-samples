from django.urls import path
from . import views

urlpatterns = [
    path('shorten', views.shortener, name='shortener'),
    # path('shorten/<str:url>', views.shortener, name='shortener'),
]