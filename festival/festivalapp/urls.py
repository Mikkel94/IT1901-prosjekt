from django.conf.urls import url
from .views import index, user_login, register, all_login_page

app_name = 'festivalapp'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', user_login, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^all_login_page/$', all_login_page, name='all_login_page'),
    url(r'^my_page/$', register, name='my_page'),

]