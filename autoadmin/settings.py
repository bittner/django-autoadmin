from __future__ import unicode_literals

from django.conf import settings

EMAIL = lambda: getattr(settings, 'AUTOADMIN_EMAIL', 'autoadmin@example.com')  # noqa: E731,E501
PASSWORD = lambda: getattr(settings, 'AUTOADMIN_PASSWORD', None)  # noqa: E731,E501
USERNAME = lambda: getattr(settings, 'AUTOADMIN_USERNAME', 'admin')  # noqa: E731,E501
