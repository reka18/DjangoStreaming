from django.urls import path
from api import views

urlpatterns = [
    path('', views.json_viewer, name='json_viewer'),
]