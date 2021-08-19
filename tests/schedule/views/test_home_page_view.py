from nails_project.nails.models import Nails
from tests.base.mixins import UserTestUtils, NailsTestUtils
from tests.base.tests import NailsProjectTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class HomePageTests(NailsProjectTestCase, UserTestUtils, NailsTestUtils):

    def test_homePageVieName_and_templateName(self):
        response = self.client.get(reverse('home page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='nails/index.html')

