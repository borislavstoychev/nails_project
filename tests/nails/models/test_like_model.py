from nails_project.nails.models import Feedback, Like
from tests.base.mixins import UserTestUtils, NailsTestUtils
from tests.base.tests import NailsProjectTestCase
from django.core.exceptions import ValidationError


class LikeModelTests(NailsTestUtils, UserTestUtils, NailsProjectTestCase):

    def test_saveModel_whenValid_shouldBeValid(self):
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True)
        nails = self.create_nails(
            type=Feedback.MANICURE,
            feedback='Test',
            description='Test nails description',
            image='path/to/image.png',
            user=nails_user,
        )
        data = {
            'nails': nails,
            'user': self.user,
        }
        obj = Like(**data)
        obj.full_clean()
        obj.save()
        self.assertEqual(nails, obj.nails)
        self.assertEqual(self.user, obj.user)
        self.assertTrue(Like.objects.filter(nails_id=nails.id).exists())

    def test_saveModel_whenInvalid_shouldBeInvalid(self):
        nails = self.create_nails(
            type=Feedback.MANICURE,
            feedback='Test',
            description='Test nails description',
            image='path/to/image.png',
            user=self.user,
        )
        data = {
            'nails': nails,
        }
        with self.assertRaises(ValidationError) as error:
            like = Like(**data)
            like.full_clean()
            like.save()
        self.assertIsNotNone(error)
        self.assertNotEqual(nails.like_set, 0)
        self.assertFalse(Like.objects.filter(nails_id=nails.id).exists())