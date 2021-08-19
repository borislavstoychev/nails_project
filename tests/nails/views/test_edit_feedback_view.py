from django.urls import reverse

from nails_project.nails.models import Feedback
from tests.base.mixins import NailsTestUtils, UserTestUtils
from tests.base.tests import NailsProjectTestCase


class NailsEditTest(NailsTestUtils, UserTestUtils, NailsProjectTestCase):

    def test_editNails_whenNailsDoesNotExists_shouldBeNotFound(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('feedback edit', kwargs={
            'pk': 1,
        }))

        self.assertEqual(404, response.status_code)

    def test_editNails_whenNailsExistsAndIsOwner_shouldReturnDetailsForNails(self):
        self.client.force_login(self.user)
        nails = self.create_feedback(
            type=Feedback.MANICURE,
            feedback=Feedback.POSITIVE,
            description='Test nails description',
            image='path/to/image.png',
            user=self.user,
        )

        response = self.client.post(reverse('feedback edit', kwargs={
            'pk': nails.id,
        }), data={
            "type": 'Manicure',
            'feedback': 'Negative',
            'description': 'TEst nails description',
            'image': 'path/to/image.png',
            'use': self.user,
        })

        self.assertEqual(302, response.status_code)

        nails_exists = Feedback.objects.filter(
            feedback='Negative'
        ) \
            .exists()

        self.assertTrue(nails_exists)
        self.assertEqual(f'/feedback-details/{nails.id}/', response.url)

    def test_editNails_whenNailsExistsAndNotOwner_shouldReturnForbidden(self):
        self.client.force_login(self.user)
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True)
        nails = self.create_feedback(
            type=Feedback.MANICURE,
            feedback='Test',
            description='Test nails description',
            image='path/to/image.png',
            user=nails_user,
        )

        response = self.client.get(reverse('feedback edit', kwargs={
            'pk': nails.id,
        }), data={
            "type": 'Manicure',
            'feedback': 'positive',
            'description': 'TEst nails description',
            'image': 'path/to/image.png',
            'use': nails_user,
        })

        self.assertEqual(403, response.status_code)

        nails_exists = Feedback.objects.filter(
            feedback='positive'
        ) \
            .exists()

        self.assertFalse(nails_exists)
