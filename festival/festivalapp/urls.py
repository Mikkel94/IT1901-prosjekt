from django.conf.urls import url
from . import views

app_name = 'festivalapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^concert_list/$', views.list_concert, name='list_concert'),
    url(r'^manager/(?P<pk>\d+)/$', views.manager, name='manager'),
    url(r'^booking_responsible/$', views.booking_responsible, name='booking_responsible'),
    url(r'^booking/(?P<pk>\d+)/add$', views.book_band, name='booking'),
    url(r'^bands/(?P<pk>\d+)/remove/$', views.delete_band, name='delete_band'),
    url(r'^old_festivals/$', views.show_previous_festivals, name='old_festivals'),
    url(r'^set_audience/(?P<pk>\d+)/change$', views.set_audience, name='set_audience'),
    url(r'^set_exp/(?P<pk>\d+)/change$', views.set_albums_and_former_concerts, name='set_exp'),
    url(r'^search/$', views.search, name='search')
]
