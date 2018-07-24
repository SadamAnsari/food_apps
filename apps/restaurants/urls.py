from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^add/$', views.add_restaurants, name='add_restaurant'),
    url(r'^list/$', views.view_restaurants, name='view_restaurant'),
    url(r'^edit/(?P<id>\d+)$', views.update_restaurant, name='update_restaurant'),
    url(r'^delete/(?P<id>\d+)$', views.delete_restaurant, name='delete_restaurant'),
    url(r'^items/add/$', views.add_food_item, name='add_food_item')
]