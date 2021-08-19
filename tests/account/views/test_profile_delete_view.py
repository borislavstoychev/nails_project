from django.urls import reverse
from nails_project.accounts.models import Profile
from tests.base.mixins import NailsTestUtils, UserTestUtils
from tests.base.tests import NailsProjectTestCase


class ProfileDeleteTest(NailsTestUtils, UserTestUtils, NailsProjectTestCase):

    def test_deleteProfileVieName_and_templateName(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile delete', kwargs={"pk":self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='account/profile/profile_delete.html')

    def test_deleteProfile_whenProfileDoesNotExists_shouldBeNotFound(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('profile delete', kwargs={
            'pk': 5,
        }))

        self.assertEqual(404, response.status_code)

    def test_deleteProfile_whenProfileExistsAndIsOwner_shouldReturnSingUpView(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('profile delete', kwargs={
            'pk': self.user.id,
        }))

        self.assertEqual(302, response.status_code)

        nails_exists = Profile.objects.filter(
            pk=self.user.id
        ) \
            .exists()

        self.assertFalse(nails_exists)
        self.assertEqual('/profile/sign-up/', response.url)

    def test_deleteProfiles_whenProfilesExistsAndNotOwner_shouldReturnForbidden(self):
        self.client.force_login(self.user)
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True)

        response = self.client.get(reverse('profile delete', kwargs={
            'pk': nails_user.id,
        }))

        self.assertEqual(403, response.status_code)

        nails_exists = Profile.objects.filter(
            pk=nails_user.id
        ) \
            .exists()

        self.assertTrue(nails_exists)