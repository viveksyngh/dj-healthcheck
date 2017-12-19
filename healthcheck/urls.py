from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^api/$', views.health_check, name='api'),
]

