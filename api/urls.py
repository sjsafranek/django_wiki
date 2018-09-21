from django.urls import path

from . import views

urlpatterns = [
    path('v1/ping', views.ping, name='ping'),
    path('v1/page', views.api, name='api'),
]
