from django.conf.urls import url
from festApp import views

urlpatterns = [
    # Index page / login
    url(r'^$', views.login, name='login')
]