from __future__ import unicode_literals

import logging

from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from south.signals import post_migrate

from .models import AutoAdminSingleton
from .settings import EMAIL, PASSWORD, USERNAME, ENABLE

logger = logging.getLogger(__name__)


@receiver(post_migrate, dispatch_uid='autoadmin_create')
def autoadmin_create(sender, **kwargs):
    """
    Create our own admin super user automatically whenever the post migrate
    signal is triggered.
    """

    if kwargs['app'] == 'autoadmin':
        # Only create the auto admin once, on our own post migrate signal
        AutoAdminSingleton.objects.get_or_create()

        if ENABLE:
            try:
                auth_models.User.objects.get(username=USERNAME)
            except auth_models.User.DoesNotExist:
                logger.info('Creating super admin user -- login: %s, password: %s' % (USERNAME, PASSWORD))
                assert auth_models.User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
                admin = auth_models.User.objects.get(username=USERNAME)

                # Store the auto admin password properties to display the first login message
                autoadmin_properties, created = AutoAdminSingleton.objects.get_or_create()
                autoadmin_properties.account = admin
                autoadmin_properties.password = PASSWORD
                autoadmin_properties.password_hash = admin.password
                autoadmin_properties.save()
            else:
                logger.info('Super admin user already exists. -- login: %s' % USERNAME)


@receiver(post_save, dispatch_uid='autoadmin_account_passwd_change', sender=User)
def autoadmin_account_passwd_change(sender, instance, **kwargs):
    autoadmin_properties = AutoAdminSingleton.objects.get()
    if instance == autoadmin_properties.account and instance.password != autoadmin_properties.password_hash:
        # Only delete the auto admin properties if the password was changed
        autoadmin_properties.account = None
        autoadmin_properties.password = None
        autoadmin_properties.password_hash = None
        autoadmin_properties.save()
