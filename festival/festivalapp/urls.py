from django.conf.urls import url
from .views import index, user_login, register, list_concert, temp

app_name = 'festivalapp'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', user_login, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^temp/$', temp, name='temp'),
    url(r'^concert_list/$', list_concert, name='list_concert')

]
