from os.path import join
from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
from nails_project import settings
from nails_project.nails.models import Nails
from tests.base.tests import NailsProjectTestCase
import random
from django.core.exceptions import ValidationError


class TestNailsModel(NailsProjectTestCase):
    path_to_image = join(settings.BASE_DIR, 'tests', 'media', 'test.jpg')
    file_name = f'{random.randint(1, 10000)}-test.jpg'

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_saveModel_whenValid_shouldBeValid(self):
        data = {
            'type': Nails.MANICURE,
            'feedback': Nails.POSITIVE,
            'description': "description",
            'image': SimpleUploadedFile(
                name=self.file_name,
                content=open(self.path_to_image, 'rb').read(),
                content_type='image/jpeg',
            ),
            "user": self.user

        }
        obj = Nails(**data)
        obj.full_clean()
        obj.save()
        self.assertEqual('Manicure', obj.type)
        self.assertEqual('Positive', obj.feedback)
        self.assertEqual('description', obj.description)
        self.assertEqual('jpg', obj.image.format)
        self.assertEqual(self.user, obj.user)

    def test_saveModel_whenInvalid_shouldBeInvalid_imageError(self):
        data = {
            'type': Nails.MANICURE,
            'feedback': Nails.POSITIVE,
            'description': "description",
            'image': None,
            "user": self.user,
        }

        with self.assertRaises(ValidationError) as error:
            obj = Nails(**data)
            obj.full_clean()
            obj.save()
        self.assertIsNotNone(error)
        self.assertFalse(Nails.objects.filter(pk=obj.id).exists())

    def test_saveModel_whenInvalid_shouldBeInvalid_descriptionError(self):
        data = {
            'type': Nails.MANICURE,
            'feedback': Nails.POSITIVE,
            'description': None,
            'image': 'image.jpg',
            "user": self.user,
        }

        with self.assertRaises(ValidationError) as error:
            obj = Nails(**data)
            obj.full_clean()
            obj.save()
        self.assertIsNotNone(error)
        self.assertFalse(Nails.objects.filter(pk=obj.id).exists())

    def test_saveModel_whenInvalid_shouldBeInvalid_userError(self):
        data = {
            'type': Nails.MANICURE,
            'feedback': Nails.POSITIVE,
            'description': "description",
            'image': "None",
            "user": None,
        }

        with self.assertRaises(ValidationError) as error:
            obj = Nails(**data)
            obj.full_clean()
            obj.save()
        self.assertIsNotNone(error)
        self.assertFalse(Nails.objects.filter(pk=obj.id).exists())

    def test_saveModel_whenInvalid_shouldBeInvalid_feedbackError(self):
        data = {
            'type': Nails.MANICURE,
            'feedback': None,
            'description': "description",
            'image': 'image.jpg',
            "user": self.user,
        }

        with self.assertRaises(ValidationError) as error:
            obj = Nails(**data)
            obj.full_clean()
            obj.save()
        self.assertIsNotNone(error)
        self.assertFalse(Nails.objects.filter(pk=obj.id).exists())

    def test_saveModel_whenInvalid_shouldBeInvalid_typeError(self):
        data = {
            'type': None,
            'feedback': Nails.POSITIVE,
            'description': "description",
            'image': 'image.jpg',
            "user": self.user,
        }

        with self.assertRaises(ValidationError) as error:
            obj = Nails(**data)
            obj.full_clean()
            obj.save()
        self.assertIsNotNone(error)
        self.assertFalse(Nails.objects.filter(pk=obj.id).exists())
