from django.conf.urls import url
from . import views

app_name = 'festivalapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^concert_list/$', views.list_concert, name='list_concert'),
    url(r'^manager/$', views.manager, name='manager'),
    url(r'^booking_responsible/$', views.booking_responsible, name='booking_responsible'),
    url(r'^booking/(?P<pk>\d+)/add$', views.book_band, name='booking'),
    url(r'^bands/(?P<pk>\d+)/remove/$', views.delete_band, name='delete_band'),
    url(r'^old_festivals/$', views.show_previous_festivals, name='old_festivals'),
    url(r'^generate_price/(?P<calc>\w+)/$', views.generate_price, name="generate_price"),
    url(r'^set_audience/(?P<pk>\d+)/change$', views.set_audience, name='set_audience'),
    url(r'^review/(?P<pk>\d+)/change$', views.add_review, name='add_review'),
    url(r'^set_exp/(?P<pk>\d+)/change$', views.set_albums_and_former_concerts, name='set_exp'),
    url(r'^search/$', views.search, name='search'),
    url(r'^booking_requests/$', views.booking_requests, name='booking_requests'),
    url(r'^accept_booking/(?P<pk>\d+)/accept$', views.accept_booking_request, name='accept_booking_request'),
    url(r'^accept_booking/(?P<pk>\d+)/delete$', views.decline_booking_request, name='decline_booking_request'),
    url(r'^booking_requests/(?P<pk>\d+)/cancel$', views.cancel_booking_request, name='cancel_booking_request'),
    url(r'^assign_tech/(?P<tech_pk>\d+)/(?P<concert_pk>\d+)/', views.assign_tech_to_concert, name='assign_tech'),
]
