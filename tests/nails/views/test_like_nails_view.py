from django.urls import reverse

from nails_project.nails.models import Nails, Like
from tests.base.mixins import UserTestUtils, NailsTestUtils
from tests.base.tests import NailsProjectTestCase


class LikePetViewTests(NailsTestUtils, UserTestUtils, NailsProjectTestCase):
    def test_likeNails_whenNailsNotLiked_shouldCreateLike(self):
        self.client.force_login(self.user)
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True)
        nails = self.create_nails(
            type=Nails.MANICURE,
            feedback='Test',
            description='Test nails description',
            image='path/to/image.png',
            user=nails_user,
        )

        response = self.client.get(reverse('like nails', kwargs={
            'pk': nails.id,
        }))

        self.assertEqual(302, response.status_code)

        like_exists = Like.objects.filter(
            user_id=self.user.id,
            nails_id=nails.id,
        ) \
            .exists()

        self.assertTrue(like_exists)

    def test_likeNails_whenNailsAlreadyLiked_shouldDeleteTheLike(self):
        self.client.force_login(self.user)
        nails_user = self.create_user(email='pet@user.com', password='12345qwe', is_active=True)
        nails = self.create_nails_with_like(
            like_user=self.user,
            type=Nails.MANICURE,
            feedback='Test',
            description='TEst nails description',
            image='path/to/image.png',
            user=nails_user,
        )

        response = self.client.get(reverse('like nails', kwargs={
            'pk': nails.id,
        }))

        self.assertEqual(302, response.status_code)

        like_exists = Like.objects.filter(
            user_id=self.user.id,
            nails_id=nails.id,
        ) \
            .exists()

        self.assertFalse(like_exists)

    def test_likeNails_whenNails_userIsOwner_shouldBeForbidden(self):
        self.client.force_login(self.user)
        nails = self.create_nails_with_like(
            like_user=self.user,
            type=Nails.MANICURE,
            feedback='Test',
            description='TEst nails description',
            image='path/to/image.png',
            user=self.user,
        )

        response = self.client.get(reverse('like nails', kwargs={
            'pk': nails.id,
        }))

        self.assertEqual(403, response.status_code)
