from nails_project.accounts.models import Profile
from tests.base.tests import NailsProjectTestCase
from django.core.exceptions import ValidationError


class ProfileModelTests(NailsProjectTestCase):

    def test_Model_whenUser_noProfileData(self):
        data = {
            'first_name': 'Borislav'
        }
        obj = Profile.objects.get(pk=self.user.id)

        self.assertEqual('', obj.first_name)
        self.assertEqual('', obj.last_name)
        self.assertEqual('', obj.phone_number)
        self.assertEqual(None, obj.age)
        self.assertEqual(self.user, obj.user)
        self.assertTrue(Profile.objects.filter(pk=self.user.id).exists())