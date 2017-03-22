from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^process2$', views.process2),
    url(r'^like/(?P<post_id>\d+)$', views.like),
    url(r'^like2/(?P<post_id>\d+)$', views.like2),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^delete2/(?P<id>\d+)$', views.delete2),
    url(r'^popular$', views.popular)
]
