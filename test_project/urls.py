from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^accounts/login/$', auth_views.LoginView.as_view()),
    url(r'^mock_view/', views.mock_view, name='mock_view'),
]
