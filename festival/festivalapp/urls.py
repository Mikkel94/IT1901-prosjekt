from django.conf.urls import url
from .views import index, user_login, register, list_concert, user_logout, manager

app_name = 'festivalapp'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^concert_list/$', list_concert, name='list_concert'),
    url(r'^manager/$', manager, name='manager')

]
