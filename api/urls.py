__author__ = 'christian.cecilia1@gmail.com'
from django.conf.urls import patterns,url
from api import views

urlpatterns = [
    #Pages
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/(?P<user_uid>[^/]+)/$', views.dashboard, name='dashboard'),
    url(r'^profile/(?P<user_uid>[^/]+)/$', views.profile, name='profile'),
    url(r'^email/verification/(?P<user_uid>[^/]+)/$', views.emailVerification, name='emailVerification'),

    #Ajax
    url(r'^registerUser/$', views.registerUser, name='registerUser'),
    url(r'^loginAjax/$', views.loginAjax, name='loginAjax'),
    url(r'^addMainGroup/$', views.addMainGroup, name='addMainGroup'),
]