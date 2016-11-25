from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^comment/new/$', views.comment_add, name='comment_add'),
    url(r'^comment/reply/$', views.comment_reply, name='comment_reply'),
]
