from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^/(?P<testapp_id>\d+)$', views.show, name='show'),
    url(r'^/(?P<testapp_id>\d+)/urlendsinslash/$', views.slashed, name='slashed'),
    url(r'^/url\+with\+plus$', views.plused, name='plused'),
    url(r'^/quoted/(?P<slug>[^/]+)$', views.quoted, name='quoted'),
]
