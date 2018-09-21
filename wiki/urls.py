from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^.*/delete', views.deletePageHandler, name='delete_page'),
    url(r'^.*/edit', views.editPageHandler, name='edit_page'),
    url(r'^.*', views.viewPageHandler, name='view_page'),
]
