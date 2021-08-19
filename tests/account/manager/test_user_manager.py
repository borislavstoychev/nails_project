from tests.base.mixins import UserTestUtils, ScheduleTestUtils
from tests.base.tests import NailsProjectTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class NailsUserManagerTests(NailsProjectTestCase):

    def test_createUser_shouldReturnUser(self):
        nails_user = UserModel.objects.create_user(email='nails@user.com', password='12345qwe')

        self.assertEqual(False, nails_user.is_active)
        self.assertEqual(False, nails_user.is_staff)
        self.assertEqual('nails@user.com', nails_user.email)

    def test_createSuperUser_shouldReturnSuperUser(self):
        nails_user = UserModel.objects.create_superuser(email='nails@user.com', password='12345qwe')

        self.assertEqual(True, nails_user.is_active)
        self.assertEqual(True, nails_user.is_staff)
        self.assertEqual('nails@user.com', nails_user.email)
