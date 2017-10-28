"""
Authentication adapters for Allauth
"""
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _

ADMIN_EMAIL_ADDRESSES = [email for name, email in settings.ADMINS]


class AutoadminAccountAdapter(DefaultAccountAdapter):
    """
    Allauth account adapter that enables automatic grant of admin permissions
    to users signing up having their email address listed in the ``ADMINS``
    Django settings.  Django settings needed to activate this feature:

        INSTALLED_APPS = [
            'django.contrib.auth',
            'django.contrib.sites',
            'allauth',
            'allauth.account',
            'allauth.socialaccount',
        ]

        ACCOUNT_ADAPTER = 'autoadmin.auth.allauth.AutoadminAccountAdapter'

    See also:
    - http://django-allauth.readthedocs.io/en/latest/configuration.html
    - http://django-allauth.readthedocs.io/en/latest/advanced.html#admin
    """

    def confirm_email(self, request, email_address):
        """
        Give superuser privileges automagically if the email address of a
        user confirming their email is listed in ``settings.ADMINS``.
        """
        super().confirm_email(request, email_address)

        if email_address.email in ADMIN_EMAIL_ADDRESSES:
            user = email_address.user
            user.is_staff = user.is_superuser = True
            user.save()

            messages.add_message(
                request, messages.INFO,
                _('Welcome Admin! You have been given superuser privileges. '
                  'Use them with caution.')
            )
