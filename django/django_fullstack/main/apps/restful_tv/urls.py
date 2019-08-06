from django.conf.urls import url
from . import views

urlpatterns= [
    url(r'^$', views.root),
    url(r'^shows/new', views.add),
    url(r'^shows$', views.show),
    url(r'^shows/(?P<id>\d+)/edit$', views.edit),
    url(r'^shows/(?P<id>\d+)$', views.display),
    url(r'^shows/(?P<id>\d+)/delete$', views.delete),
    url(r'^shows/(?P<id>\d+)/update$', views.update),
    url(r'^fresh$', views.fresh),
]