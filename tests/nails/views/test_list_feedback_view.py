from django.urls import reverse
from nails_project.nails.models import Feedback
from tests.base.mixins import UserTestUtils, NailsTestUtils
from tests.base.tests import NailsProjectTestCase


class NailsListViewTest(NailsTestUtils, UserTestUtils,NailsProjectTestCase):

    def test_NailsListVieName_and_templateName(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('feedback list'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='nails/feedback_list.html')

    def test_getList_whenLoggedInUserWithNoNails_shouldGetListWithNoNails(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('feedback list'))
        self.assertListEmpty(list(response.context['nails']))

    def test_getList_whenNotLoggedInUserWithNoNails_shouldGetListWithNoNails(self):
        response = self.client.get(reverse('feedback list'))
        self.assertListEmpty(list(response.context['nails']))

    def test_getList_whenLoggedInUserWithNails_shouldGetListWithNails(self):
        self.client.force_login(self.user)
        nails = self.create_feedback(
            type=Feedback.MANICURE,
            feedback='Test',
            description='Test nails description',
            image='path/to/image.png',
            user=self.user,
        )
        nails2 = self.create_feedback(
            type=Feedback.MANICURE,
            feedback='Test2',
            description='Test2 nails description',
            image='path/to/image.png',
            user=self.user,
        )

        response = self.client.get(reverse('feedback list'))
        self.assertEqual(2, len(list(response.context['nails'])))

    def test_getList_whenNotLoggedInUserWithNails_shouldGetListWithNails(self):
        nails = self.create_feedback(
            type=Feedback.MANICURE,
            feedback='Test',
            description='Test nails description',
            image='path/to/image.png',
            user=self.user,
        )
        nails2 = self.create_feedback(
            type=Feedback.MANICURE,
            feedback='Test2',
            description='Test2 nails description',
            image='path/to/image.png',
            user=self.user,
        )

        response = self.client.get(reverse('feedback list'))
        self.assertEqual(2, len(list(response.context['nails'])))