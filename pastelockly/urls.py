from django.urls import path
from . import views

urlpatterns = [
    path('pastelockly', views.saveToDb, name="saveToDb"),
    path('pastelockly/<int:id>', views.getPaste, name="getPaste"),
]