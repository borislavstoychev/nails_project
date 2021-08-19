from unittest.mock import patch
from os.path import join
import random
from django.contrib.auth import get_user_model
from django.urls import reverse
from nails_project import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from nails_project.nails.models import Feedback
from tests.base.tests import NailsProjectTestCase

UserModel = get_user_model()


class SignalsNails(NailsProjectTestCase):

    @patch('django.db.models.signals.ModelSignal.send')
    def test_nailsSave_oldImagesDeleteIfExist(self, mock):
        path_to_image = join(settings.BASE_DIR, 'tests', 'media', 'test.jpg')
        file_name = f'{random.randint(1, 10000)}-test.jpg'
        file = SimpleUploadedFile(
            name=file_name,
            content=open(path_to_image, 'rb').read(),
            content_type='image/jpeg')
        self.client.force_login(self.user)

        response = self.client.post(reverse('feedback create'), data={
            "type": Feedback.MANICURE,
            'feedback': Feedback.POSITIVE,
            'description': 'TEst nails description',
            'image': file,
            'user': self.user
        })

        # Check that your signal was called.
        self.assertTrue(mock.called)