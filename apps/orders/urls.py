from __future__ import unicode_literals, absolute_import
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^order/add_order/$', views.add_order, name="add_order"),
    url(r'^order/add_cart/$', views.add_cart, name="add_cart")
]
