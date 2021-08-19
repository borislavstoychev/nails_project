from nails_project.nails.models import Feedback, Like
from tests.base.mixins import UserTestUtils, NailsTestUtils
from tests.base.tests import NailsProjectTestCase
from django.core.exceptions import ValidationError


class LikeModelTests(NailsTestUtils, UserTestUtils, NailsProjectTestCase):

    def test_saveModel_whenValid_shouldBeValid(self):
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True)
        feedback = self.create_feedback(
            type=Feedback.MANICURE,
            feedback='Test',
            description='Test nails description',
            image='path/to/image.png',
            user=nails_user,
        )
        data = {
            'feedback': feedback,
            'user': self.user,
        }
        obj = Like(**data)
        obj.full_clean()
        obj.save()
        self.assertEqual(feedback, obj.feedback)
        self.assertEqual(self.user, obj.user)
        self.assertTrue(Like.objects.filter(feedback_id=feedback.id).exists())

    def test_saveModel_whenInvalid_shouldBeInvalid(self):
        feedback = self.create_feedback(
            type=Feedback.MANICURE,
            feedback='Test',
            description='Test nails description',
            image='path/to/image.png',
            user=self.user,
        )
        data = {
            'feedback': feedback,
        }
        with self.assertRaises(ValidationError) as error:
            like = Like(**data)
            like.full_clean()
            like.save()
        self.assertIsNotNone(error)
        self.assertNotEqual(feedback.like_set, 0)
        self.assertFalse(Like.objects.filter(feedback_id=feedback.id).exists())