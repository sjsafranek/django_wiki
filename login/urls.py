# from django.urls import path
from django.conf.urls import url

# Import auth_views for login and logout methods
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # url(r'^login', auth_views.login),
    # url(r'^logout', auth_views.logout, { "next_page" : '/login'}),
    url(r'^login', auth_views.LoginView),
    url(r'^logout', auth_views.LogoutView, { "next_page" : '/login'}),

    url(r'^check_permissions', views.checkPermissionsHandler),

    # https://simpleisbetterthancomplex.com/tutorial/2016/09/19/how-to-create-password-reset-view.html
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
