from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^comment/new/$', views.CommentAddView.as_view(), name='comment_add'),
    url(r'^comment/reply/$', views.CommentReplyView.as_view(), name='comment_reply'),
]
