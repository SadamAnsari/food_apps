from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profile/$', views.user_profile, name='profile'),
    # url(r'^profile/(?P<id>\d+)/$', views.update_profile, name='profile'),
]
