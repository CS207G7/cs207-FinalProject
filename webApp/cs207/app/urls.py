from django.conf.urls import url

from app import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  # url(r'^main/$', views.main, name='main'),
  url(r'^filters/$', views.filters, name='filters'),
  url(r'^docs/$', views.docs, name='docs'),
]