from nails_project.nails.models import Feedback
from tests.base.mixins import UserTestUtils, NailsTestUtils
from tests.base.tests import NailsProjectTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class AboutPageTests(NailsProjectTestCase, UserTestUtils, NailsTestUtils):

    def test_homePageVieName_and_templateName(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='nails/about.html')

