from django.conf.urls import url
from .views import index, user_login, register, list_concert,\
    user_logout, manager, booking_responsible, book_band, delete_band

app_name = 'festivalapp'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^concert_list/$', list_concert, name='list_concert'),
    url(r'^manager/$', manager, name='manager'),
    url(r'^booking_responsible/$', booking_responsible, name='booking_responsible'),
    url(r'^booking/(?P<pk>\d+)/add$', book_band, name='booking'),
    url(r'^bands/(?P<pk>\d+)/remove/$', delete_band, name='delete_band'),
]
