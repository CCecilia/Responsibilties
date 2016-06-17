__author__ = 'christian.cecilia1@gmail.com'
from django.conf.urls import patterns,url
from api import views

urlpatterns = [
    #Pages
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/(?P<user_uid>[^/]+)/$', views.dashboard, name='dashboard'),

    #Ajax
    url(r'^registerUser/$', views.registerUser, name='registerUser'),
    url(r'^loginAjax/$', views.loginAjax, name='loginAjax'),
]