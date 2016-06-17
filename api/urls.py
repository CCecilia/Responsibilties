__author__ = 'christian.cecilia1@gmail.com'
from django.conf.urls import patterns,url
from api import views

urlpatterns = [
    #Pages
    url(r'^$', views.index, name='index'),

    #Ajax
    url(r'^registerUser/$', views.registerUser, name='registerUser'),
]