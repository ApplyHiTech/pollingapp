from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^index', views.index, name='index'),
	url(r'^first', views.first, name='first'),
	url(r'^second',views.second, name='second')
]