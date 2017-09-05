"""serialbox URL Configuration
"""
from django.conf.urls import include, url
from rest_framework import urls as rf_urls
from serialbox.api import urls as api_urls

urlpatterns = [
    url(r'^', include(api_urls)),
    url(r'^auth/', include(rf_urls, namespace='rest_framework')),
]
