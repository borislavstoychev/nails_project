from django.urls import reverse

from nails_project.nails.models import Feedback, Like
from tests.base.mixins import NailsTestUtils, UserTestUtils
from tests.base.tests import NailsProjectTestCase


class NailsDetailsTest(NailsTestUtils, UserTestUtils, NailsProjectTestCase):

    def test_NailsDetailsVieName_and_templateName(self):
        self.client.force_login(self.user)
        nails = self.create_feedback(
            type=Feedback.MANICURE,
            feedback='Test',
            description='Test nails description',
            image='path/to/image.png',
            user=self.user,
        )
        response = self.client.get(reverse('feedback details', kwargs={'pk': nails.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='nails/feedback_details.html')

    def test_getNailsDetails_whenNailsDoesNotExists(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('feedback details', kwargs={
            'pk': 1,
        }))

        self.assertEqual(404, response.status_code)

    def test_getNailsDetails_whenNailsExistsAndIsOwner_shouldReturnDetailsForNails(self):
        self.client.force_login(self.user)
        nails = self.create_feedback(
            type=Feedback.MANICURE,
            feedback='Test',
            description='TEst nails description',
            image='path/to/image.png',
            user=self.user,
        )

        response = self.client.get(reverse('feedback details', kwargs={
            'pk': nails.id,
        }))

        self.assertTrue(response.context['is_owner'])
        self.assertFalse(response.context['is_liked_by_user'])

    def test_getNailsDetails_whenNailsExistsAndIsNotOwnerAndNotLiked_shouldReturnDetailsForNails(self):
        self.client.force_login(self.user)
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True)
        nails = self.create_feedback(
            type=Feedback.MANICURE,
            feedback='Test',
            description='TEst nails description',
            image='path/to/image.png',
            user=nails_user,
        )

        response = self.client.get(reverse('feedback details', kwargs={
            'pk': nails.id,
        }))

        self.assertFalse(response.context['is_owner'])
        self.assertFalse(response.context['is_liked_by_user'])
        self.assertEqual(0, nails.like_set.count())

    def test_getNailsDetails_whenNailsExistsAndIsNotOwnerAndLiked_shouldReturnDetailsForNails(self):
        self.client.force_login(self.user)
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True)
        nails = self.create_feedback_with_like(
            like_user=self.user,
            type=Feedback.MANICURE,
            feedback='Test',
            description='TEst nails description',
            image='path/to/image.png',
            user=nails_user,
        )

        response = self.client.get(reverse('feedback details', kwargs={
            'pk': nails.id,
        }))

        self.assertFalse(response.context['is_owner'])
        self.assertTrue(response.context['is_liked_by_user'])
        self.assertEqual(1, nails.like_set.count())


