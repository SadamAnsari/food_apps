from __future__ import unicode_literals, absolute_import
from django.conf.urls import url
from . import views

app_name = "apps.login"

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^change_password$', views.change_password, name='change_password'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^signup/validate_username/$', views.validate_username, name='validate_username'),
]
