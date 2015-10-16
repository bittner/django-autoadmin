from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core import management
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings

from autoadmin.models import AutoAdminSingleton
from autoadmin.settings import USERNAME

from .literals import (
    TEST_ADMIN_USER_EMAIL, TEST_ADMIN_USER_PASSWORD, TEST_ADMIN_USER_USERNAME,
    TEST_FIRST_TIME_LOGIN_TEXT, TEST_MOCK_VIEW_TEXT
)

TEST_GENERATED_PASSWORD = 'generated password'


def password_generator():
    return TEST_GENERATED_PASSWORD


class AutoAdminHandlerTestCase(TestCase):
    def setUp(self):
        AutoAdminSingleton.objects.create_autoadmin()

    def tearDown(self):
        AutoAdminSingleton.objects.all().delete()

    def test_post_admin_creation(self):
        self.assertEqual(AutoAdminSingleton.objects.get().account.username, USERNAME())

        user = AutoAdminSingleton.objects.get().account

        user.set_password(TEST_ADMIN_USER_PASSWORD)
        user.save(update_fields=('password',))

        self.assertEqual(AutoAdminSingleton.objects.get().account, None)


class AutoAdminManagementCommandTestCase(TestCase):
    def setUp(self):
        management.call_command('createautoadmin', interactive=False)

    def tearDown(self):
        AutoAdminSingleton.objects.all().delete()

    def test_autoadmin_creation(self):
        autoadmin = AutoAdminSingleton.objects.get()
        user = get_user_model().objects.first()

        self.assertEqual(AutoAdminSingleton.objects.count(), 1)

        self.assertEqual(autoadmin.account, user)
        self.assertEqual(autoadmin.account.email, user.email)
        self.assertEqual(autoadmin.password_hash, user.password)


class AutoAdminModelTestCase(TestCase):
    def setUp(self):
        AutoAdminSingleton.objects.create_autoadmin()

    def tearDown(self):
        AutoAdminSingleton.objects.all().delete()

    def test_double_creation(self):
        self.assertEqual(AutoAdminSingleton.objects.count(), 1)
        AutoAdminSingleton.objects.create_autoadmin()
        self.assertEqual(AutoAdminSingleton.objects.count(), 1)


class AutoAdminSettingsTestCase(TestCase):
    def setUp(self):
        AutoAdminSingleton.objects.all().delete()

    def tearDown(self):
        AutoAdminSingleton.objects.all().delete()

    @override_settings(AUTOADMIN_EMAIL=TEST_ADMIN_USER_EMAIL)
    def test_autoadmin_email(self):
        AutoAdminSingleton.objects.create_autoadmin()
        self.assertEqual(AutoAdminSingleton.objects.get().account.email, TEST_ADMIN_USER_EMAIL)

    @override_settings(AUTOADMIN_PASSWORD=TEST_ADMIN_USER_PASSWORD)
    def test_autoadmin_password(self):
        AutoAdminSingleton.objects.create_autoadmin()
        self.assertEqual(AutoAdminSingleton.objects.get().password, TEST_ADMIN_USER_PASSWORD)

    @override_settings(AUTOADMIN_PASSWORD=password_generator)
    def test_autoadmin_password_function(self):
        AutoAdminSingleton.objects.create_autoadmin()
        self.assertEqual(AutoAdminSingleton.objects.get().password, TEST_GENERATED_PASSWORD)

    @override_settings(AUTOADMIN_USERNAME=TEST_ADMIN_USER_USERNAME)
    def test_autoadmin_email(self):
        AutoAdminSingleton.objects.create_autoadmin()
        self.assertEqual(AutoAdminSingleton.objects.get().account.username, TEST_ADMIN_USER_USERNAME)


class AutoAdminViewCase(TestCase):
    def setUp(self):
        AutoAdminSingleton.objects.create_autoadmin()

    def tearDown(self):
        AutoAdminSingleton.objects.all().delete()

    def test_login_302_view(self):
        response = self.client.get(reverse('mock_view'), follow=True)

        self.assertContains(
            response, text=TEST_FIRST_TIME_LOGIN_TEXT,
            status_code=200
        )

    def test_login_ok_view(self):
        autoadmin = AutoAdminSingleton.objects.get()
        logged_in = self.client.login(
            username=autoadmin.account, password=autoadmin.password
        )

        response = self.client.get(reverse('mock_view'), follow=True)

        self.assertContains(
            response, text=TEST_MOCK_VIEW_TEXT,
            status_code=200
        )

    def test_error_handling_at_login_view(self):
        AutoAdminSingleton.objects.all().delete()

        response = self.client.get(reverse('mock_view'), follow=True)

        self.assertContains(
            response, text='',
            status_code=200
        )

    def test_autoadmin_properties_tag(self):
        autoadmin = AutoAdminSingleton.objects.get()

        response = self.client.get(reverse('mock_view'), follow=True)

        self.assertContains(
            response, text='autoadmin_properties_username: %s' % (
                autoadmin.account.username
            ), status_code=200
        )
