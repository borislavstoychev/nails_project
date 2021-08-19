from nails_project.accounts.models import NailsUser
from tests.base.tests import NailsProjectTestCase
from django.core.exceptions import ValidationError


class UserNailsModelTests(NailsProjectTestCase):

    def test_saveModel_whenValid_shouldBeValid(self):

        data = {
            'email': 'testuser@mail.bg',
            "password": 'testuser12345'
        }
        obj = NailsUser(**data)
        obj.full_clean()
        obj.save()
        self.assertEqual('testuser@mail.bg', obj.email)
        self.assertEqual(False, obj.is_active)
        self.assertEqual(False, obj.is_staff)
        self.assertTrue(NailsUser.objects.filter(email='testuser@mail.bg').exists())

    def test_saveModel_whenInvalid_shouldBeInvalid_emailError(self):

        data = {
            'email': None,
            "password": 'testuser12345'
        }
        with self.assertRaises(ValidationError) as error:
            obj = NailsUser(**data)
            obj.full_clean()
            obj.save()
        self.assertIsNotNone(error)
        self.assertEqual(False, obj.is_active)
        self.assertFalse(NailsUser.objects.filter(email='testuser@mail.bg').exists())

    def test_saveModel_whenInvalid_shouldBeInvalid_passwordError(self):

        data = {
            'email': 'testuser@mail.bg',
            "password": None
        }
        with self.assertRaises(ValidationError) as error:
            obj = NailsUser(**data)
            obj.full_clean()
            obj.save()
        self.assertIsNotNone(error)
        self.assertEqual(False, obj.is_active)
        self.assertFalse(NailsUser.objects.filter(email='testuser@mail.bg').exists())

