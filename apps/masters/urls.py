from __future__ import unicode_literals, absolute_import
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ajax/states/$', views.get_states, name='get_states'),
    url(r'^ajax/cities/$', views.get_cities, name='get_cities'),
]
