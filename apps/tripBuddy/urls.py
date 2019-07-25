from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^new$', views.new),
    url(r'^trips/new', views.newTrip),
    url(r'^trips/remove_trip/(?P<trip_id>\d+)$', views.remove_trip, name='remove_trip'),
    url(r'^trips/(?P<trip_id>\d+)$', views.show_trip, name='show_trip'),
    url(r'^trips/edit/(?P<trip_id>\d+)$', views.edit_trip, name='edit_trip'),
    url(r'^edit/(?P<trip_id>\d+)$', views.edit, name='edit'),
    url(r'^trips/add_trip/(?P<trip_id>\d+)$', views.add_trip, name='add_trip'),
    url(r'^trips/giveup/(?P<trip_id>\d+)$', views.giveup_trip, name='giveup_trip'),
]