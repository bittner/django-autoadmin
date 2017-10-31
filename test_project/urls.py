from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^accounts/login/$', auth_views.login),
    url(r'^mock_view/', views.mock_view, name='mock_view'),
]

try:
    # Django <= 1.9 uses `patterns`
    from django.conf.urls import patterns
    urlpatterns = patterns('', *urlpatterns)
except ImportError:
    pass
