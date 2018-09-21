
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^file', views.uploadFileHandler),
]
