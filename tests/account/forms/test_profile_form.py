from nails_project.accounts.forms import ProfileForm
from tests.base.tests import NailsProjectTestCase
from os.path import join
import random
from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
from nails_project import settings


class TestProfileForm(NailsProjectTestCase):

    path_to_image = join(settings.BASE_DIR, 'tests', 'media', 'test.jpg')
    file_name = f'{random.randint(1, 10000)}-test.jpg'
    file_data = {'image': SimpleUploadedFile(
        name=file_name,
        content=open(path_to_image, 'rb').read(),
        content_type='image/jpeg',
    )}

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_saveForm_whenValid_shouldBeValid(self):
        data = {
            'first_name': "Borislav",
            'Last_name': 'Stoychev',
            'phone_number': '0878799823',
            'age': '19',
        }
        form = ProfileForm(data, self.file_data)
        self.assertTrue(form.is_valid())

    def test_saveForm_whenInValid_shouldBeInValid_firstNameError(self):
        data = {
            'first_name': "Borislav12345678912345",
            'Last_name': 'Stoychev',
            'phone_number': '0878799823',
            'age': '19',
        }
        form = ProfileForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('first_name'))

    def test_saveForm_whenInValid_shouldBeInValid_lastNameError(self):
        data = {
            'first_name': "Borislav",
            'last_name': 'Stoychev12345678912345654545445555655555555555555555556655',
            'phone_number': '0878799823',
            'age': '19',
        }
        form = ProfileForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('last_name'))

    def test_saveForm_whenInValid_shouldBeInValid_phoneNumberError(self):
        data = {
            'first_name': "Borislav",
            'last_name': 'Stoychev',
            'phone_number': '08787brb9823',
            'age': '19',
        }
        form = ProfileForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('phone_number'))
