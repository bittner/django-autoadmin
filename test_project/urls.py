from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^accounts/login/$', auth_views.login),
    url(r'^mock_view/', 'test_project.views.mock_view', name='mock_view'),
)
