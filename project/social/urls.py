from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^comment/new/$', views.comment_add, name='comment_add'),
    url(r'^comment/reply/$', views.comment_reply, name='comment_reply'),
    # url(r'^comments/json/(?P<page>[0-9]+)/', views.comments_json, name='comments_json')
]
