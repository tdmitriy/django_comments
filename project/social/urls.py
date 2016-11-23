from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^$comments/new/$', views.comment_add, name='comment_add'),
    # url(r'^comments/json/(?P<page>[0-9]+)/', views.comments_json, name='comments_json')
]
