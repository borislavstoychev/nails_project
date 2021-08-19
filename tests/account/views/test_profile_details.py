import random
from os.path import join

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from nails_project.accounts.models import Profile
from nails_project.nails.models import Nails
from tests.base.mixins import UserTestUtils
from tests.base.tests import NailsProjectTestCase


class ProfileUpdateDetailsTest(UserTestUtils, NailsProjectTestCase):

    def test_profileDetailsVieName_and_templateName(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile details', kwargs={"pk": self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='account/profile/profile_details.html')

    def test_getDetails_whenLoggedInUserWithNoNails_shouldGetDetailsWithNoNails(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile details', kwargs={'pk': self.user.id}))
        self.assertListEmpty(list(response.context['nails']))
        self.assertEqual(self.user.id, response.context['profile'].user_id)

    def test_getDetails_whenLoggedInUserWithFeedback_shouldGetDetails(self):
        nails = Nails.objects.create(
            type=Nails.MANICURE,
            feedback='Test',
            description='TEst nails description',
            image='path/to/image.png',
            user=self.user,
        )

        self.client.force_login(self.user)

        response = self.client.get(reverse('profile details', kwargs={'pk': self.user.id}))

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.user.id, response.context['profile'].user_id)
        self.assertListEqual([nails], list(response.context['nails']))

    def test_postDetails_whenUserLoggedInWithoutImage_shouldChangeImage(self):
        path_to_image = join(settings.BASE_DIR, 'tests', 'media', 'test.jpg')

        file_name = f'{random.randint(1, 10000)}-test.jpg'
        file = SimpleUploadedFile(
            name=file_name,
            content=open(path_to_image, 'rb').read(),
            content_type='image/jpeg')

        self.client.force_login(self.user)

        response = self.client.post(reverse('profile details', kwargs={'pk': self.user.id}), data={
            'profile_image': file,
        })

        self.assertEqual(302, response.status_code)

        profile = Profile.objects.get(pk=self.user.id)
        self.assertTrue(str(profile.profile_image.format).endswith('jpg'))

    def test_postDetails_whenUserLoggedInWithImage_shouldChangeImage(self):
        path_to_image = join(settings.BASE_DIR, 'tests', 'media', 'test.jpg')
        profile = Profile.objects.get(pk=self.user.id)
        profile.profile_image = path_to_image
        profile.save()

        self.client.force_login(self.user)

        response = self.client.post(reverse('profile details', kwargs={'pk': self.user.id}), data={
            'profile_image': path_to_image,
        })

        self.assertEqual(302, response.status_code)

        profile = Profile.objects.get(pk=self.user.id)
        image = path_to_image.split("/").pop()
        profile_image = str(profile.profile_image).split("/").pop()+'.jpg'

        self.assertEqual(image, profile_image)

    def test_postDetails_whenUserLoggedInWithoutData_shouldUpdateData(self):
        path_to_image = join(settings.BASE_DIR, 'tests', 'media', 'test.jpg')
        profile = Profile.objects.get(pk=self.user.id)
        profile.profile_image = path_to_image
        profile.save()

        self.client.force_login(self.user)

        response = self.client.post(reverse('profile details', kwargs={'pk': self.user.id}), data={
            'profile_image': path_to_image,
            'first_name': 'Borislav',
            'last_name': 'Stoychev',
            'phone_number': '0878799548',
            'age': 21
        })

        self.assertEqual(302, response.status_code)

        profile = Profile.objects.get(pk=self.user.id)
        image = path_to_image.split("/").pop()
        profile_image = str(profile.profile_image).split("/").pop()+'.jpg'

        self.assertEqual(image, profile_image)
        self.assertEqual('Borislav', profile.first_name)
        self.assertEqual("Stoychev", profile.last_name)
        self.assertEqual(['0878799548'], [profile.phone_number])
        self.assertEqual(21, profile.age)
