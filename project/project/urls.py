from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('social.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
]
