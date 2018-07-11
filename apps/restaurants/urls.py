from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^add/$', views.add_restaurants, name='add_restaurant'),
    url(r'^list/$', views.view_restaurants, name='view_restaurant'),
]