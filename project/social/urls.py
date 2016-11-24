from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^comment/post/$', views.comment_add, name='comment_add'),
    url(r'^comment/json/(?P<page>[0-9]+)/(?P<per_page>[0-9]+)/', views.json_comments, name='json_comments'),
]
