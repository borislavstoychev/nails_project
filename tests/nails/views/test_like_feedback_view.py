from django.urls import reverse

from nails_project.nails.models import Feedback, Like
from tests.base.mixins import UserTestUtils, NailsTestUtils
from tests.base.tests import NailsProjectTestCase


class LikePetViewTests(NailsTestUtils, UserTestUtils, NailsProjectTestCase):
    def test_likeNails_whenNailsNotLiked_shouldCreateLike(self):
        self.client.force_login(self.user)
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True)
        feedback = self.create_feedback(
            type=Feedback.MANICURE,
            feedback='Test',
            description='Test nails description',
            image='path/to/image.png',
            user=nails_user,
        )

        response = self.client.get(reverse('feedback like', kwargs={
            'pk': feedback.id,
        }))

        self.assertEqual(302, response.status_code)

        like_exists = Like.objects.filter(
            user_id=self.user.id,
            feedback_id=feedback.id,
        ) \
            .exists()

        self.assertTrue(like_exists)

    def test_likeNails_whenNailsAlreadyLiked_shouldDeleteTheLike(self):
        self.client.force_login(self.user)
        nails_user = self.create_user(email='pet@user.com', password='12345qwe', is_active=True)
        feedback = self.create_feedback_with_like(
            like_user=self.user,
            type=Feedback.MANICURE,
            feedback='Test',
            description='TEst nails description',
            image='path/to/image.png',
            user=nails_user,
        )

        response = self.client.get(reverse('feedback like', kwargs={
            'pk': feedback.id,
        }))

        self.assertEqual(302, response.status_code)

        like_exists = Like.objects.filter(
            user_id=self.user.id,
            feedback_id=feedback.id,
        ) \
            .exists()

        self.assertFalse(like_exists)

    def test_likeNails_whenNails_userIsOwner_shouldBeForbidden(self):
        self.client.force_login(self.user)
        feedback = self.create_feedback_with_like(
            like_user=self.user,
            type=Feedback.MANICURE,
            feedback='Test',
            description='TEst nails description',
            image='path/to/image.png',
            user=self.user,
        )

        response = self.client.get(reverse('feedback like', kwargs={
            'pk': feedback.id,
        }))

        self.assertEqual(403, response.status_code)
