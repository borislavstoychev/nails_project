from os.path import join
import random

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from nails_project import settings
from nails_project.nails.models import Nails
from tests.base.mixins import NailsTestUtils, UserTestUtils
from tests.base.tests import NailsProjectTestCase


class NailsCreateTest(NailsTestUtils, UserTestUtils, NailsProjectTestCase):

    def test_NailsCreateVieName_and_templateName(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('create nails'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='nails/nails_create.html')

    def test_createNails_whenUserExist_shouldRedirectToNailsDetails(self):
        path_to_image = join(settings.BASE_DIR, 'tests', 'media', 'test.jpg')
        file_name = f'{random.randint(1, 10000)}-test.jpg'
        file = SimpleUploadedFile(
            name=file_name,
            content=open(path_to_image, 'rb').read(),
            content_type='image/jpeg')
        self.client.force_login(self.user)

        response = self.client.post(reverse('create nails'), data={
            "type": Nails.MANICURE,
            'feedback': Nails.POSITIVE,
            'description': 'TEst nails description',
            'image': file,
            'user': self.user
        })
        self.assertEqual(302, response.status_code)
        self.assertEqual(Nails.objects.last().feedback, "Positive")

    def test_creatNails_whenUserNotExist_shouldBeRedirectToSignIn(self):
        data = {
            "type": 'Manicure',
            'feedback': 'Test',
            'description': 'TEst nails description',
            'image': 'path/to/image.png',
            'use': self.user,
        }

        response_get = self.client.get(reverse('create nails'))
        self.assertEqual(302, response_get.status_code)
        self.assertEqual('/profile/sign-in/?next=/create/', response_get.url)
