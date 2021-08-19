from django.urls import reverse

from nails_project.nails.models import Feedback
from tests.base.mixins import NailsTestUtils, UserTestUtils
from tests.base.tests import NailsProjectTestCase


class NailsDeleteTest(NailsTestUtils, UserTestUtils, NailsProjectTestCase):

    def test_NailsDeleteVieName_and_templateName(self):
        self.client.force_login(self.user)
        nails = self.create_nails(
            type=Feedback.MANICURE,
            feedback='Test',
            description='Test nails description',
            image='path/to/image.png',
            user=self.user,
        )
        response = self.client.get(reverse('feedback delete', kwargs={'pk': nails.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='nails/feedback_delete.html')

    def test_deleteNails_whenNailsDoesNotExists_shouldBeNotFound(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('feedback delete', kwargs={
            'pk': 1,
        }))

        self.assertEqual(404, response.status_code)

    def test_deleteNails_whenNailsExistsAndIsOwner_shouldReturnAllNails(self):
        self.client.force_login(self.user)
        nails = self.create_nails(
            type=Feedback.MANICURE,
            feedback='Test',
            description='Test nails description',
            image='path/to/image.png',
            user=self.user,
        )

        response = self.client.post(reverse('feedback delete', kwargs={
            'pk': nails.id,
        }))

        self.assertEqual(302, response.status_code)

        nails_exists = Feedback.objects.filter(
            id=nails.id
        ) \
            .exists()

        self.assertFalse(nails_exists)
        self.assertEqual('/feedback/', response.url)

    def test_deleteNails_whenNailsExistsAndNotOwner_shouldReturnForbidden(self):
        self.client.force_login(self.user)
        nails_user = self.create_user(email='nails@user.com', password='12345qwe', is_active=True)
        nails = self.create_nails(
            type=Feedback.MANICURE,
            feedback='Test',
            description='Test nails description',
            image='path/to/image.png',
            user=nails_user,
        )

        response = self.client.get(reverse('feedback delete', kwargs={
            'pk': nails.id,
        }))

        self.assertEqual(403, response.status_code)

        nails_exists = Feedback.objects.filter(
            id=nails.id
        ) \
            .exists()

        self.assertTrue(nails_exists)
